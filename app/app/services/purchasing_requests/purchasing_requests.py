from datetime import datetime, timedelta
from sqlalchemy.orm import Session, joinedload
from fastapi import HTTPException
from app.models.purchases.purchasing_requests import PurchasingRequests
from app.models.purchases.purchases import Purchases
from app.models.users.users import Users
from app.models.aboniments.aboniments import Aboniments
from app.models.packages.packages import AbonimentPackage
from app.web.schemas.purchases.purchases import PurchasesStatuses as purchase_statuses
from app.app.schemas.purchasing_requests import purchasing_requests as sc


def add_purchasing_request(db: Session, request: sc.PurchasingRequestAdd, user: Users):
    aboniment: Aboniments = db.query(Aboniments).filter_by(id=request.aboniment_id,
                                                           is_deleted=False).first()
    if not aboniment:
        raise HTTPException(400, detail={
            "detail": "Aboniment not found!",
            "error_title": "Validation error"
        })

    # check if user already has a pending or approved purchasing request for this aboniment
    existing_request = (
        db
        .query(PurchasingRequests)
        .filter(PurchasingRequests.user_id == user.id,
                PurchasingRequests.aboniment_id == aboniment.id,
                PurchasingRequests.status.in_(['new']))
        .first()
    )
    if existing_request:
        raise HTTPException(400, detail={
            "detail": "You have already requested this aboniment",
            "error_title": "Validation error"
        })

    if not user.department or not user.department.strip():
        if request.department and request.department.strip():
            user.department = request.department.strip()
            db.add(user)
            db.commit()
            db.refresh(user)
        return {"department": "is mepty"}

    # check active purchase for same aboniment
    now = datetime.now()
    active_purchases = (
        db
        .query(Purchases)
        .filter(Purchases.user_id == user.id,
                Purchases.aboniment_id == aboniment.id,
                Purchases.status == purchase_statuses.NEW)
        .all()
    )

    unused_count = 0
    for p in active_purchases:
        package = (
            db
            .query(AbonimentPackage)
            .filter(AbonimentPackage.id == aboniment.aboniment_package_id)
            .first()
        )
        if not package:
            continue

        expiry_date = p.recorded_date + timedelta(days=package.expiry_days)

        if expiry_date < now or p.used_count >= package.count:
            p.status = purchase_statuses.USED
            db.add(p)
            continue

        unused_count += max(0, package.count - p.used_count)

    if unused_count > 0:
        db.commit()
        raise HTTPException(400, detail={
            "detail": f"You already have {unused_count} unused active aboniment(s) for this plan",
            "error_title": "Validation error"
        })

    # if we marked any expired/used purchases as USED, commit those updates
    if active_purchases:
        db.commit()

    new_request = PurchasingRequests(
        user_id = user.id,
        aboniment_id = aboniment.id,
        purchase_id = None,
    )
    
    db.add(new_request)
    try:
        db.commit()
        return {"result": "Ok"}
    except Exception as err:
        db.rollback()
        raise HTTPException(400, detail={
            "detail": str(err),
            "error_title": "Database error"
        })


def get_user_requests(db: Session, user: Users):
    resp = (
        db
        .query(PurchasingRequests)
        .filter_by(user_id=user.id,
                   is_deleted=False)
        .options(joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.aboniment_package),
                 joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.provider))
        .order_by(PurchasingRequests.id.desc())
        .all()
    )
    return resp

def get_new_purchasing_requests(db: Session, user: Users):
    resp = (
        db
        .query(PurchasingRequests)
        .filter(PurchasingRequests.is_deleted == False,
                PurchasingRequests.purchase_id == None,
                PurchasingRequests.status == sc.PurchasingRequestsStatus.NEW)
        .options(joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.aboniment_package),
                 joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.provider),
                 joinedload(PurchasingRequests.user))
        .order_by(PurchasingRequests.id.desc())
        .all()
    )
    return resp

def get_all_purchasing_requests(db: Session, user: Users):
    resp = (
        db
        .query(PurchasingRequests)
        .filter_by(is_deleted=False)
        .options(joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.aboniment_package),
                 joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.provider),
                 joinedload(PurchasingRequests.user))
        .order_by(PurchasingRequests.id.desc())
        .all()
    )
    return resp