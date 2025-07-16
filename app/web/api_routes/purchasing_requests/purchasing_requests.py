import logging
from fastapi import APIRouter, Query
from app.web.schemas.purchasing_requests import purchasing_requests as sc
from app.web.services.purchasing_requests import purchasing_requests as sv
from app.app.schemas.purchasing_requests import purchasing_requests as app_sc
from app.helpers.auth import provider_auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/web/purchasing-requests', tags=['Purchasing requests'])


@router.get('/get-news', status_code=200, response_model=sc.ListGetRequestsResponse)
def get_api(admin=provider_auth()):
    return sv.get_new_purchasing_requests(admin=admin)


@router.post('/set/{request_id}', status_code=200)
def post_api(request_id: int,
             status: str = Query(..., description=(
                 "Status should be one of :"
                f"``{app_sc.PurchasingRequestsStatus.ACCESSED}`` | "
                f"``{app_sc.PurchasingRequestsStatus.DENIED}``"
             )),
             admin=provider_auth()):
    return sv.set_purchasing_request_status(request_id=request_id, status=status, admin=admin)
