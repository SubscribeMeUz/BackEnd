from datetime import date, datetime
from fastapi import APIRouter, Query
from typing import List

from app.web.services.statistics import statistics as sv
from app.web.schemas.statistics import statistics as sc
from app.web.schemas.statistics.statistics import UserAbonimentUseRequest, UserAbonimentUseResponse
from app.helpers.auth import auth


router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get('/get-daily-purchases')
def get_daily_purchases(from_date: datetime = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD"),
                        provider_id: int = None, _=auth()):
    return sv.get_daily_purchases(provider_id=provider_id,
                                  from_date=from_date, to_date=to_date)


@router.get('/get-active-aboniments')
def get_active_aboniments(from_date: date = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD", le= date.today()),
                        provider_id: int = None, _=auth()):
    return sv.get_active_aboniments(provider_id=provider_id,
                                  from_date=from_date, to_date=to_date)


@router.get('/get-user-aboniment-uses')
def get_user_aboniment_uses(from_date: date = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD"),
                        provider_id: int = None, _=auth()):
    return sv.get_user_aboniment_uses(provider_id=provider_id,
                                      from_date=from_date, to_date=to_date)


@router.get('/get-uses-with-time')
def get_uses_with_time(from_date: date = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD"),
                        provider_id: int = None,
                        interval_hours: sc.LiteralHoursInterval = 1, _=auth()):
    return sv.get_uses_with_time(provider_id=provider_id,
                                 from_date=from_date, to_date=to_date, interval_hours=int(interval_hours))


@router.post('/get-user-list-by-usetimes', response_model=List[UserAbonimentUseResponse])
def get_user_list_by_usetimes(user_request: UserAbonimentUseRequest, user=auth()): 
    return sv.get_user_list_by_usetimes(user_request=user_request, user=user)

@router.post('/get-purchase-history', response_model=List[sc.PurchaseHistoryResponse])
def get_purchase_history(purchase_request: sc.PurchaseHistoryRequest, user =auth()):
    return sv.get_purchase_history(purchase_request=purchase_request, user=user)