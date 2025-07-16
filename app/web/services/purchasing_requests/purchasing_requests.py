import logging
from sqlalchemy.orm import Session, joinedload
from app.models.purchases.purchasing_requests import PurchasingRequests
from app.models.users.users import Users
from app.models.purchases.purchases import Purchases
from app.models.aboniments.aboniments import Aboniments
from app.models.providers.providers import Providers
from app.app.schemas.purchasing_requests import purchasing_requests as app_sc
from app.web.services.purchases import purchases as purchases_service
from app.web.schemas.users.roles import Roles


logger = logging.getLogger(__name__)


def get_new_purchasing_requests(db: Session, admin: Users):
    resp = (
        db
        .query(PurchasingRequests)
        .options(joinedload(PurchasingRequests.user),
                 joinedload(PurchasingRequests.aboniment)
                 .options(joinedload(Aboniments.aboniment_package),
                          joinedload(Aboniments.provider))
                 )
        .filter(PurchasingRequests.status == app_sc.PurchasingRequestsStatus.NEW)
    )
    if admin.role != Roles.admin:
        resp = resp.filter(
            PurchasingRequests.aboniment.has(
                Aboniments.provider.has(
                    Providers.owner_id == admin.id
                )
            )
        )

    resp = (
        resp
        .order_by(PurchasingRequests.id.desc())
        .all()
    )
    return resp


def set_purchasing_request_status(db: Session,
                                  request_id: int,
                                  status: app_sc.PurchasingRequestsStatuses,
                                  admin: Users):
    request: PurchasingRequests = db.query(PurchasingRequests).filter_by(id=request_id).first()
    if not (admin.role == Roles.admin or request.aboniment.provider.owner_id == admin.id):
        raise ValueError("Bu so'rovga javob bermaysiz!")
    if not request:
        raise ValueError("Not found!")
    old_status = request.status
    if status == app_sc.PurchasingRequestsStatus.ACCESSED:
        purchase_add = purchases_service.PurchasePostRequest(aboniment_id=request.aboniment_id,
                                           user_id=request.user_id)
        purchases_service.add_purchase(request=purchase_add)
    elif status == app_sc.PurchasingRequestsStatus.NEW:
        raise ValueError("Bu statusni ortga qaytarish foydasiz va mumkin emas!")
    else:
        pass
    request.status = status
    db.add(request)
    try:
        db.commit()
        return {"result": "Ok",
                "message": f"Status changed to `{request.status}` from `{old_status}`"}
    except Exception as err:
        logger.error(err)
        raise ValueError(f"Error: {err}")
