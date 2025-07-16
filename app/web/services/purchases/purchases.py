import math
from datetime import datetime
from sqlalchemy.orm import Session, joinedload
from app.models.purchases.purchases import Purchases
from app.models.aboniments.aboniments import Aboniments
from app.models.providers.providers import Providers
from app.models.users.users import Users
from app.web.schemas.purchases.purchases import PurchasePostRequest
from app.web.schemas.users.roles import Roles


def _get_purchase(db: Session, purchase_id: int) -> Purchases:
    resp = (
        db
        .query(Purchases)
        .options(joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider)
                    .joinedload(Providers.owner),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.aboniment_package),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.workout_time),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider_tab),
                 joinedload(Purchases.user))
        .filter(Purchases.id == purchase_id)
        .first()
    )
    if not resp:
        raise ValueError("Not found")
    return resp


def get_purchase(db: Session, purchase_id: int):
    return _get_purchase(db=db, purchase_id=purchase_id)


def get_filtered_purchases(db: Session,
                           aboniment_id: int,
                           page: int,
                           page_size: int,
                           date: datetime,
                           user_id: int = None,
                           owner: Users = None):
    offset = (page - 1) * page_size
    
    query = (
        db
        .query(Purchases)
        .options(joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider)
                    .joinedload(Providers.owner),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.aboniment_package),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider_tab),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.workout_time),
                 joinedload(Purchases.user))
    )
    if owner.role != Roles.admin:
        query = query.filter(Purchases.aboniment.provider.owner_id == owner.id)
    if date:
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        query = (
            query
            .filter(
                Purchases.recorded_date >= start,
                Purchases.recorded_date <= end
            )
        )
    if aboniment_id:
        aboniment = db.query(Aboniments).filter(Aboniments.id == aboniment_id).first()
        if not aboniment:
            raise ValueError("Aboniment not found!")
        query = (
            query
            .filter(
                Purchases.aboniment_id == aboniment_id,
            )
        )
    if user_id:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise ValueError("User not found!")
        query = query.filter(Purchases.user_id == user_id)
    total = query.count()
    resp = (
        query
        .order_by(Purchases.recorded_date)
        .offset(offset=offset)
        .limit(limit=page_size)
        .all()
    )
    return {
        "total": total,
        "total_pages": math.ceil(total / page_size),
        "page": page,
        "page_size": page_size,
        "data": resp
    }


def get_user_purchases(db: Session,
                       user: Users,
                       page: int,
                       page_size: int,
                       date: datetime):
    offset = (page - 1) * page_size
    resp = (
        db
        .query(Purchases)
        .options(joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider)
                    .joinedload(Providers.owner),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.aboniment_package),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.provider_tab),
                 joinedload(Purchases.aboniment)
                    .joinedload(Aboniments.workout_time),
                 joinedload(Purchases.user))
        .filter(Purchases.user_id == user.id)
    )
    if date:
        start = datetime.combine(date, datetime.min.time())
        end = datetime.combine(date, datetime.max.time())
        resp = (
            resp
            .filter(
                Purchases.recorded_date >= start,
                Purchases.recorded_date <= end
            )
        )
    total = resp.count()
    resp = (
        resp
        .order_by(Purchases.recorded_date)
        .offset(offset=offset)
        .limit(limit=page_size)
        .all()
    )
    return {
        "total": total,
        "total_pages": math.ceil(total / page_size),
        "page": page,
        "page_size": page_size,
        "data": resp
    }


def add_purchase(db: Session, request: PurchasePostRequest):
    purchase = Purchases()
    purchase.user_id = request.user_id
    purchase.aboniment_id = request.aboniment_id

    db.add(purchase)
    try:
        db.commit()
        db.refresh(purchase)
        return {"result": "Ok",
                "purchase": _get_purchase(db=db, purchase_id=purchase.id)}
    except Exception as err:
        db.rollback()
        raise err
