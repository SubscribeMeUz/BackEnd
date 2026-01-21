import math
import uuid
import shutil
import logging
from datetime import datetime, timedelta
from fastapi import UploadFile
from typing import List
from sqlalchemy.orm import Session, joinedload, Query
from app.models.users.users import Users
from app.models.aboniments.aboniments import Aboniments
from app.models.purchases.purchases import Purchases
from app.models.providers.providers import Providers
from app.models.photos.photos import Photos
from app.web.schemas.providers.providers import ProviderOut
from app.web.schemas.users.roles import Roles
from geopy.geocoders import Nominatim


logger = logging.getLogger(__name__)


def get_all_providers(db: Session, owner: Users):
    resp = db.query(Providers)

    if owner.role != Roles.admin:
        resp = resp.filter(Providers.owner_id == owner.id)
    resp = resp.options(joinedload(Providers.owner)).all()

    return resp

def get_provider_by_name(db: Session, provider_name: str) -> List[Providers]:
    resp = db.query(Providers).options(joinedload(Providers.owner))
    
    if provider_name:
        resp = resp.filter(Providers.name.ilike(f"%{provider_name}%"))
    
    resp = resp.all()
    return resp

def get_new_providers(db: Session) -> List[Providers]:
    two_weeks_ago = datetime.utcnow() - timedelta(weeks=2)
    resp = (
        db
        .query(Providers)
        .options(joinedload(Providers.owner))
        .filter(Providers.registred_date >= two_weeks_ago)
        .order_by(Providers.registred_date.desc())
        .limit(10)
        .all()
    )
    return resp

def get_all_providers_with_filters(
        db: Session,
        page: int,
        page_size: int,
        string_query: str,
        owner: Users
):
    resp: Query = (
        db
        .query(Providers)
        .options(joinedload(Providers.owner))
    )
    if owner.role != Roles.admin:
        resp = resp.filter(Providers.owner_id == owner.id)

    if string_query:
        resp = resp.filter(
            Providers.name.ilike(f"{string_query}"),
        )
    total_count = resp.count()
    total_count = 1
    offset = (page - 1) * page_size
    resp = (
        resp
        .order_by(Providers.registred_date)
        .offset(offset)
        .limit(page_size)
        .all()
    )

    return {
        "total": total_count,
        "page": page,
        "total_page": math.ceil(total_count / page_size),
        "limit": page_size,
        "data": resp
    }


def get_provider(db: Session, provider_id: int):
    return _get_provider(db=db, provider_id=provider_id)


def _get_provider(db: Session, provider_id: int) -> Providers:
    resp: Providers = (
        db
        .query(Providers)
        .options(joinedload(Providers.owner),
                 joinedload(Providers.aboniments),
                 joinedload(Providers.aboniment_packages),
                 joinedload(Providers.workout_times),
                 joinedload(Providers.provider_tabs),
                 joinedload(Providers.photos))
        .filter(Providers.id == provider_id)
        .first()
    )
    if not resp:
        raise ValueError("Provider not found!")
    setattr(resp, "pic_hours", [])
    return resp


def get_about_more_provider(provider_id: int):
    resp = _get_provider(provider_id=provider_id)
    return resp


def get_providers_related_by_user(db: Session, user: Users):
    resp = (
        db
        .query(Providers)
        .options(joinedload(Providers.owner))
        .join(Providers.aboniments)
        .join(Aboniments.purchases)
        .filter(Purchases.user_id == user.id)
        .all()
    )
    return resp


def get_providers_by_owner(db: Session, owner_id: int):
    resp = (
        db
        .query(Providers)
        .options(joinedload(Providers.owner))
        .filter(Providers.owner_id == owner_id)
        .all()
    )
    return resp


def add_provider(db: Session,
                 name: str,
                 location_latt: str,
                 location_long: str,
                 necessary_tools: str,
                 about_description: str,
                 logo_path: str,
                 owner_id: int):
    pv = Providers(
        name = name,
        location_latt = location_latt,
        location_long = location_long,
        location_name = get_location_name(location_latt, location_long),
        necessary_tools = necessary_tools,
        about_description = about_description,
        logo_path = logo_path,
        owner_id = owner_id,
    )
    try:
        db.add(pv)
        db.commit()
        db.refresh(pv)
        return {"result": "Ok", "provider": ProviderOut.model_validate(pv)}
    except Exception as err:
        db.rollback()
        logger.error(err)
        raise err


def get_location_name(lat: float, lon: float) -> str:
    try:
        geolocator = Nominatim(user_agent="u.shermetov11197@gmail.com")
        location = geolocator.reverse((lat, lon), language='en')
        if location:
            return location.address
    except Exception as err:
        logger.error(err)
    return "Unknown location"


def edit_provider(db: Session,
                  provider_id: int,
                  name: str,
                  location_latt: str,
                  location_long: str,
                  about_description: str,
                  logo_path: str,
                  owner_id: int):
    provider: Providers = db.query(Providers).options(
        joinedload(Providers.owner)).filter(Providers.id == provider_id).first()
    if name:
        provider.name = name
    if location_latt:
        provider.location_latt = location_latt
        provider.location_long = location_long
    if logo_path:
        provider.logo_path = logo_path
    if about_description:
        provider.about_description = about_description
    if owner_id:
        provider.owner_id = owner_id
    
    db.add(provider)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {
        "result": "Ok",
        "message": "Edited!"
    }


def delete_provider(db: Session, provider_id: int):
    provider = db.query(Providers).filter(Providers.id == provider_id).first()
    try:
        db.delete(provider)
        db.commit()
        return {'result': 'ok'}
    except Exception as err:
        return {'result': 'failed', 'error': f'{err}'}


def save_provider_photo(db: Session, provider_id: int, photo: str):
    provider = _get_provider(db=db, provider_id=provider_id)
    limit = 10
    if len(provider.photos) >= limit:
        raise ValueError(f"Limit is {limit}!")
    p = Photos(
        path = photo,
        provider_id = provider_id
    )
    db.add(p)
    try:
        db.commit()
        return {
            "result": "Ok",
            "photo": p.path
        }
    except Exception as err:
        db.rollback()
        raise err


def delete_photo(db: Session, photo_id: int):
    photo = db.query(Photos).filter_by(id=photo_id).first()
    try:
        db.delete(photo)
    except Exception as err:
        db.rollback()
        raise err
    return {"result": 'Ok'}


def save_file(file: UploadFile):
    "returns url endpoint"
    if file:
        filename = str(uuid.uuid4())+'-' + file.filename
        out_file_path = f"app/static/images/{filename}"
        with open(out_file_path, 'wb') as out_file:
            shutil.copyfileobj(file.file, out_file)
        return f"images/{filename}"
    else:
        return None
