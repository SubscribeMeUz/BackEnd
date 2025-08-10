from datetime import date
from fastapi import APIRouter, Query
from app.web.services.statistics import statistics as sv
from app.web.schemas.statistics import statistics as sc
from app.helpers.auth import auth


router = APIRouter(prefix='/statistics', tags=['Statistics'])


@router.get('/get-daily-purchases')
def get_daily_purchases(from_date: date = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD"),
                        provider_id: int = None, _=auth()):
    return sv.get_daily_purchases(provider_id=provider_id,
                                  from_date=from_date, to_date=to_date)


@router.get('/get-active-aboniments')
def get_active_aboniments(from_date: date = Query(None, description="YYYY-MM-DD"),
                        to_date: date = Query(None, description="YYYY-MM-DD"),
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
                        provider_id: int = None, _=auth()):
    return sv.get_uses_with_time(provider_id=provider_id,
                                 from_date=from_date, to_date=to_date)
