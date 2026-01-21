import logging
from fastapi import APIRouter
from app.app.schemas.purchasing_requests import purchasing_requests as sc
from app.app.services.purchasing_requests import purchasing_requests as sv
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/purchasing-requests', tags=['App Purchasing requests'])


@router.post('/add', status_code=200)
def post_api(request: sc.PurchasingRequestAdd, user=auth()):
    return sv.add_purchasing_request(request=request, user=user)


@router.get('/get-my-requests', status_code=200, response_model=sc.ListUserRequests)
def get_(user=auth()):
    return sv.get_user_requests(user=user)

@router.get('/get-new-requests', status_code=200)
def get_new_requests(user=auth()):
    return sv.get_new_purchasing_requests(user=user)


@router.get('/get-all-requests', status_code=200)
def get_all_requests(user=auth()):
    return sv.get_all_purchasing_requests(user=user)