import logging
from fastapi import APIRouter, Query
from typing import Optional
from datetime import datetime, date
from app.web.services.purchases import purchases as sv
from app.web.schemas.purchases import purchases as sc
from app.helpers.auth import auth, admin_auth, provider_auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/purchases", tags=['Purchases'],
                   dependencies=[auth()])


@router.get('/get', status_code=200, response_model=sc.PurchasesOut)
def get_purchases(
    aboniment_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    date_filter: Optional[date] = Query(None),
    owner = provider_auth()
):
    return sv.get_filtered_purchases(aboniment_id=aboniment_id,
                                     page=page,
                                     page_size=page_size,
                                     date=date_filter,
                                     user_id=user_id,
                                     owner=owner)


@router.get('/user-purchases', status_code=200, response_model=sc.PurchasesOut)
def get_user_purchases(page: int = Query(1, ge=1),
                       page_size: int = Query(20, le=100),
                       date_filter: Optional[date] = Query(None),
                       user=auth()):
    return sv.get_user_purchases(user=user,
                                 page=page,
                                 page_size=page_size,
                                 date=date_filter)


@router.post('/add', status_code=200, response_model=sc.PurchaseAdded)
def add_purchase(request: sc.PurchasePostRequest,
                 user=admin_auth()):
    return sv.add_purchase(request=request)
