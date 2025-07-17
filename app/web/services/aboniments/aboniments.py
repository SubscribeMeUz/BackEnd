import math
import json
import logging
import pyqrcode
from pathlib import Path
from sqlalchemy.orm import Session, joinedload
from sqlalchemy.sql import or_
from app.models.users.users import Users
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.purchases.purchases import Purchases
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.packages.packages import AbonimentPackage
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.web.schemas.users.roles import Roles
from app.web.schemas.aboniments import aboniments as sc


logger = logging.getLogger(__name__)


def get_aboniments(db: Session,
                   page: int,
                   page_size: int,
                   query: str,
                   owner: Users) -> sc.AbonimentsResponse:
    resp = (
        db
        .query(Aboniments)
        .join(Providers, Aboniments.provider)
        .join(Users, Providers.owner)
        .join(WorkOutTimes, Aboniments.workout_time)
        .join(AbonimentPackage, Aboniments.aboniment_package)
        .join(ProviderTabs, Aboniments.provider_tab)
        .filter(Aboniments.is_deleted == False,
                Providers.is_deleted == False,
                Users.is_deleted == False,
                WorkOutTimes.is_deleted == False,
                AbonimentPackage.is_deleted == False,
                ProviderTabs.is_deleted == False)
        .options(joinedload(Aboniments.provider)
                .joinedload(Providers.owner),
                joinedload(Aboniments.workout_time),
                joinedload(Aboniments.aboniment_package),
                joinedload(Aboniments.provider_tab))
    )
    if owner.role != Roles.admin:
        resp = resp.filter(Providers.owner_id == owner.id)

    if query:
        resp = (
            resp
            .join(Aboniments.provider)
            .filter(or_(
                Aboniments.name.ilike(f"%{query}%"),
                Providers.name.ilike(f"%{query}%"),
            ))
        )
    total = resp.count()

    total_pages = math.ceil(total / page_size)
    offset = (page - 1) * page_size
    resp = (
        resp
        .order_by(Aboniments.id)
        .offset(offset)
        .all()
    )
    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": page_size,
        "data": resp
    }


def get_provider_aboniments(db: Session, provider_id: int) -> sc.AbonimentsResponse:
    resp = (
        db
        .query(Aboniments)
        .join(Aboniments.provider)
        .join(Aboniments.aboniment_package)
        .join(Aboniments.provider_tab)
        .join(Aboniments.workout_time)
        .filter(Aboniments.provider_id == provider_id,
                Aboniments.is_deleted == False,
                Providers.is_deleted == False,
                AbonimentPackage.is_deleted == False,
                ProviderTabs.is_deleted == False,
                WorkOutTimes.is_deleted == False)
        .options(joinedload(Aboniments.provider)
                 .joinedload(Providers.owner),
                 joinedload(Aboniments.aboniment_package),
                 joinedload(Aboniments.provider_tab),
                 joinedload(Aboniments.workout_time))
    )
    resp = (
        resp
        .order_by(Aboniments.id)
        .all()
    )
    return resp


def get_aboniments_related_by_user(db: Session, user: Users, page: int, page_size: int):
    offset = (page - 1) * page_size
    resp = (
        db
        .query(Aboniments)
        .join(Aboniments.purchases)
        .options(joinedload(Aboniments.provider)
                 .joinedload(Providers.owner),
                 joinedload(Aboniments.provider_tab),
                 joinedload(Aboniments.workout_time),
                 joinedload(Aboniments.aboniment_package))
        .filter(Purchases.user_id == user.id)
    )
    total = resp.count()
    total_pages = math.ceil(total / page_size)
    resp = (
        resp
        .order_by(Aboniments.id)
        .offset(offset)
        .all()
    )
    return {
        "total": total,
        "total_pages": total_pages,
        "page": page,
        "limit": page_size,
        "data": resp
    }


def _get_aboniment(db: Session, aboniment_id: int):
    resp = (
        db
        .query(Aboniments)
        .join(Aboniments.provider)
        .join(Aboniments.aboniment_package)
        .join(Aboniments.provider_tab)
        .join(Aboniments.workout_time)
        .options(joinedload(Aboniments.provider)
                 .joinedload(Providers.owner),
                 joinedload(Aboniments.workout_time),
                 joinedload(Aboniments.provider_tab),
                 joinedload(Aboniments.aboniment_package))
        .filter(Aboniments.id == aboniment_id,
                Aboniments.is_deleted == False,
                Providers.is_deleted == False,
                AbonimentPackage.is_deleted == False,
                ProviderTabs.is_deleted == False,
                WorkOutTimes.is_deleted == False)
        .first()
    )
    if not resp:
        raise ValueError("Not found")
    return resp


def get_aboniment(db: Session, aboniment_id: int, owner: Users):
    aboniment = _get_aboniment(db=db, aboniment_id=aboniment_id)
    if not (aboniment.provider.owner_id == owner.id or owner.role == Roles.admin):
        raise ValueError('Not found!')
    return aboniment


def add_aboniment(db: Session, request: sc.AbonimentPost, admin: Users) -> dict:
    provider = db.query(Providers).filter_by(id=request.provider_id).first()
    if not provider:
        raise ValueError("Provider not found!")
    if not (admin.role == Roles.admin or provider.owner_id == admin.id):
        raise ValueError("Siz bu providerga aboniment qo'sha olmaysiz!")
    new_aboniment = Aboniments(
        name = request.name,
        price = request.price,
        available_days = [],
        working_hours = {},
        provider_id = request.provider_id,
        workout_time_id = request.workout_time_id,
        provider_tab_id = request.provider_tab_id,
        aboniment_package_id = request.aboniment_package_id
    )
    try:
        db.add(new_aboniment)
        db.commit()
        return {"result": "ok"}
    except Exception as err:
        db.rollback()
        raise err


def change_aboniment(db: Session, aboniment_id: int, request: sc.ChangeAboniment, owner: Users) -> dict:
    aboniment = _get_aboniment(db=db, aboniment_id=aboniment_id)
    if not (aboniment.provider.owner_id == owner.id or owner.role == Roles.admin):
        raise ValueError('Not found!')
    for field, value in request.model_dump().items():
        if value is not None:
            setattr(aboniment, field, value)

    db.add(aboniment)

    try:
        db.commit()
        db.refresh(aboniment)
        return {"result": "ok",
                "aboniment": sc.AbonimentOut.model_validate(
                    _get_aboniment(db=db, aboniment_id=aboniment_id))}
    except Exception as err:
        db.rollback()
        raise err


def delete_aboniment(db: Session, aboniment_id: int):
    aboniment = db.query(Aboniments).filter(Aboniments.id == aboniment_id,
                                            Aboniments.is_deleted == False).first()
    if not aboniment:
        raise ValueError("Not found!")
    try:
        db.delete(aboniment)
        db.commit()
        return {"result": "ok"}
    except Exception as err:
        db.rollback()
        raise err


def generate_qr_code(db: Session, aboniment_id: int = None, provider_id: int = None) -> str:
    save_dir = Path("app/static/qr_codes")

    if aboniment_id:
        aboniment: Aboniments = db.query(Aboniments).filter_by(id=aboniment_id).first()
        if not aboniment:
            raise ValueError("Aboniment not found!")
        content = {
            "aboniment_id": aboniment_id,
            "provider_id": aboniment.provider_id
        }
        file_path = save_dir / f"aboniment_{aboniment_id}.png"
    elif provider_id:
        provider = db.query(Providers).filter_by(id=provider_id).first()
        if not provider:
            raise ValueError("Provider not found!")
        content = {
            "provider_id": provider_id
        }
        file_path = save_dir / f"provider_{provider_id}.png"
    qr = pyqrcode.create(json.dumps(content))
    qr.png(str(file_path), scale=6)

    return str(file_path)
