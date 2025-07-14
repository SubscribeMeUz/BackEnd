import math
from fastapi import HTTPException, Request
from urllib.parse import urljoin
from typing import List
from sqlalchemy.orm import Session, joinedload
from datetime import datetime, timedelta
from app.models.purchases.purchases import Purchases
from app.models.aboniments.aboniments import Aboniments
from app.models.providers.providers import Providers
from app.models.users.users import Users
from app.web.schemas.purchases.purchases import PurchasePostRequest
from app.web.schemas.aboniments.aboniments import AbonimentOut
from app.app.schemas.users.users import UserOut


def add_logo_url(resp: List[Purchases] | Purchases, request: Request):
    if isinstance(resp, Purchases):
        resp.aboniment.provider.logo_url = urljoin(request.base_url.__str__(), resp.aboniment.provider.logo_path)
    else:
        for pr in resp:
            pr.aboniment.provider.logo_url = urljoin(request.base_url.__str__(), pr.aboniment.provider.logo_path)
    return resp


def get_purchase(db: Session, purchase_id: int, base_request: Request) -> Purchases:
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
    add_logo_url(resp, request=base_request)
    if not resp:
        raise ValueError("Not found")
    return resp


def get_filtered_purchases(db: Session,
                           request: Request,
                           aboniment_id: int,
                           page: int,
                           page_size: int,
                           date: datetime,
                           user_id: int = None):
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
    if date:
        print(date)
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
            raise HTTPException(404, "Aboniment not found!")
        query = (
            query
            .filter(
                Purchases.aboniment_id == aboniment_id,
            )
        )
    if user_id:
        user = db.query(Users).filter(Users.id == user_id).first()
        if not user:
            raise HTTPException(404, "User not found!")
        query = query.filter(Purchases.user_id == user_id)
    total = query.count()
    resp = (
        query
        .order_by(Purchases.recorded_date)
        .offset(offset=offset)
        .limit(limit=page_size)
        .all()
    )
    add_logo_url(resp, request=request)
    return {
        "total": total,
        "total_pages": math.ceil(total / page_size),
        "page": page,
        "page_size": page_size,
        "data": resp
    }


def get_user_purchases(db: Session,
                       request: Request,
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
    add_logo_url(resp, request=request)
    return {
        "total": total,
        "total_pages": math.ceil(total / page_size),
        "page": page,
        "page_size": page_size,
        "data": resp
    }


def add_purchase(db: Session, request: PurchasePostRequest, base_request: Request):
    purchase = Purchases()
    purchase.user_id = request.user_id
    purchase.aboniment_id = request.aboniment_id

    db.add(purchase)
    try:
        db.commit()
        db.refresh(purchase)
        return {"result": "Ok",
                "purchase": get_purchase(db=db, purchase_id=purchase.id, base_request=base_request)}
    except Exception as err:
        db.rollback()
        raise err
