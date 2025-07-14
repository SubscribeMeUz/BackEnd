from fastapi import Request
from typing import List
from urllib.parse import urljoin
from datetime import datetime, timedelta
from sqlalchemy.orm import Session, join, joinedload, contains_eager
from app.models.users.users import Users
from app.models.visitation_logs.visitation_logs import VisitationLogs
from app.models.purchases.purchases import Purchases
from app.models.aboniments.aboniments import Aboniments
from app.models.providers.providers import Providers
from app.models.packages.packages import AbonimentPackage
from app.app.schemas.visitation_logs import visitation_logs as sc
from app.web.schemas.purchases import purchases as web_purchases_sc


def add_logo_to_providers(providers: List[Providers], request: Request):
    for pr in providers:
        setattr(pr, 'logo_url', urljoin(request.base_url.__str__(),
                                        pr.logo_path))


def add_logo_url(log: VisitationLogs, request: Request):
    log.purchase.aboniment.provider.logo_url = urljoin(
        request.base_url.__str__(), log.purchase.aboniment.provider.logo_path)
    return log


def check_purchase_is_valid(db: Session, user: Users, provider_id: int, aboniment_id: int):
    if aboniment_id:
        purchase = (
            db
            .query(Purchases)
            .filter(Purchases.status == web_purchases_sc.PurchasesStatuses.NEW)
            .filter(Purchases.aboniment_id == aboniment_id)
            .filter(Purchases.user_id == user.id)
            .order_by(Purchases.recorded_date.desc())
            .first()
        )
    else:
        purchase = (
            db
            .query(Purchases)
            .join(Purchases.aboniment)
            .filter(Purchases.status == web_purchases_sc.PurchasesStatuses.NEW)
            .filter(Aboniments.provider_id == provider_id)
            .filter(Purchases.user_id == user.id)
            .order_by(Purchases.recorded_date.desc())
            .first()
        )
    if not purchase:
        raise ValueError("Sizda ushbu provayderda aktiv aboniment mavjud emas!")

    package = (
        db
        .query(AbonimentPackage)
        .join(AbonimentPackage.aboniments)
        .filter(Aboniments.id == purchase.aboniment_id)
        .first()
    )
    date_now = datetime.now()
    expire_date = purchase.recorded_date + timedelta(days=package.expiry_days)
    logs = (
        db
        .query(VisitationLogs)
        .filter(VisitationLogs.user_id == user.id,
                VisitationLogs.purchase_id == purchase.id)
        .order_by(VisitationLogs.recorded_date.desc())
    )
    visitation_count = logs.count()
    last_visitation = logs.first()
    if last_visitation and (last_visitation.recorded_date >= datetime.now() - timedelta(hours=1)):
        raise ValueError("Bir soat ichida bir nechta joydan foydalanish mumkin emas!")
    if visitation_count >= package.count:
        purchase.status = web_purchases_sc.PurchasesStatuses.USED
        try:
            db.add(purchase)
            db.commit()
        except:
            db.rollback()
        raise ValueError("Abonimentdan foydalanish limiti tugagan!")
    if expire_date.date() == date_now.date():
        raise ValueError("Bir kun ichida abonimentdan faqat bir marta foydalanish mumkin!")
    if expire_date < date_now:
        purchase.status = web_purchases_sc.PurchasesStatuses.USED
        try:
            db.add(purchase)
            db.commit()
        except:
            db.rollback()
        raise ValueError("Aboniment uchun foydalanish muddati tugagan!")
    return purchase


def get_user_visitation_log(db: Session, log_id: int, request: Request):
    resp = (
        db
        .query(VisitationLogs)
        .options(joinedload(VisitationLogs.user),
                 joinedload(VisitationLogs.purchase)
                 .joinedload(Purchases.aboniment)
                 .options(joinedload(Aboniments.provider),
                          joinedload(Aboniments.aboniment_package),
                          joinedload(Aboniments.workout_time),
                          joinedload(Aboniments.provider_tab)))
        .filter(VisitationLogs.id == log_id,
                VisitationLogs.is_deleted == False)
        .first()
    )
    add_logo_url(log=resp, request=request)
    return resp


def get_user_visitations(db: Session, user: Users,
                         http_request: Request,
                         aboniment_id: int = None,
                         provider_id: int = None):
    query = (
        db.query(Providers)
        .join(Providers.aboniments)
        .join(Aboniments.purchases)
        .join(Purchases.visitation_logs)
        .join(Aboniments.workout_time)
        .join(Aboniments.provider_tab)
        .join(Aboniments.aboniment_package)
        .filter(VisitationLogs.user_id == user.id)
    )

    if aboniment_id:
        query = query.filter(Aboniments.id == aboniment_id)

    if provider_id:
        query = query.filter(Providers.id == provider_id)

    query = query.options(
        contains_eager(Providers.aboniments)
        .options(contains_eager(Aboniments.provider_tab),
                 contains_eager(Aboniments.aboniment_package),
                 contains_eager(Aboniments.workout_time),
                 contains_eager(Aboniments.purchases)
                 .contains_eager(Purchases.visitation_logs))
    )

    providers = query.distinct(Providers.id).all()
    add_logo_to_providers(providers, http_request)
    return providers


def add_visitation_log(db: Session, request: sc.VisitationLogAddRequest, http_request: Request):
    provider = db.query(Providers).filter(Providers.id == request.provider_id).first()
    if not provider:
        raise ValueError("Provider not found")
    user = db.query(Users).filter(Users.id == request.user_id).first()
    if not user:
        raise ValueError("User not found")
    
    purchase: Purchases = check_purchase_is_valid(db=db, user=user, provider_id=request.provider_id)

    new_log = VisitationLogs(
        user_id = user.id,
        purchase_id = purchase.id
    )
    try:
        db.add(new_log)
        db.commit()
        db.refresh(new_log)
    except Exception as err:
        db.rollback()
        raise err

    return {
        "result":"Ok",
        "log": get_user_visitation_log(db=db, log_id=new_log.id, request=http_request)
    }
