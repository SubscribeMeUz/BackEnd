from sqlalchemy.orm import Session, joinedload
from app.models.purchases.purchasing_requests import PurchasingRequests
from app.models.users.users import Users
from app.models.aboniments.aboniments import Aboniments
from app.app.schemas.purchasing_requests import purchasing_requests as sc


def add_purchasing_request(db: Session, request: sc.PurchasingRequestAdd, user: Users):
    aboniment: Aboniments = db.query(Aboniments).filter_by(id=request.aboniment_id,
                                                           is_deleted=False).first()
    if not aboniment:
        raise ValueError("Aboniment not found!")
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
        raise ValueError(err)


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
        .filter_by(is_deleted=False, purchase_id=None)
        .options(joinedload(PurchasingRequests.aboniment)
                 .joinedload(Aboniments.aboniment_package),
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
                 joinedload(PurchasingRequests.user))
        .order_by(PurchasingRequests.id.desc())
        .all()
    )
    return resp