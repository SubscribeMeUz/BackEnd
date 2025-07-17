import logging
from fastapi import APIRouter, Query
from app.app.services.aboniments import aboniments as sv
from app.app.schemas.aboniments import aboniments as sc
from app.web.services.aboniments import aboniments as web_sv
from app.web.schemas.aboniments import aboniments as web_sc
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/new-aboniments", tags=['New Aboniments'])


@router.get('/get/all', status_code=200, response_model=web_sc.AbonimentsResponse)
def get_aboniments(page: int = Query(1, ge=1),
                   page_size: int = Query(20, le=100),
                   query: str = Query(None),
                   owner=auth()):
    return web_sv.get_aboniments(
        page=page,
        page_size=page_size,
        query=query,
        owner=owner
    )


@router.get('/get/my-aboniments', status_code=200, response_model=sc.ListPurchasedAboniments)
def get_aboniments(user=auth()):
    return sv.get_user_purchased_aboniments(user=user)


@router.get('/get/by-provider/{provider_id}', status_code=200, response_model=sc.ProviderAbonimentsResponse)
def get_provider_aboniments(provider_id: int, user=auth()):
    return sv.get_provider_aboniments(provider_id=provider_id)


@router.get('/get/{aboniment_id}', status_code=200, response_model=sc.AbonimentResponse)
def get_aboniment(aboniment_id: int, user=auth()):
    return web_sv.get_aboniment(aboniment_id=aboniment_id)
