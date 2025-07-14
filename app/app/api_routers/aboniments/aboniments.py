import logging
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.app.services.aboniments import aboniments as sv
from app.app.schemas.aboniments import aboniments as sc

from app.web.api_routes.aboniments import aboniments as web_aboniments


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/new-aboniments", tags=['New Aboniments'])


@router.get('/get/all', status_code=200,)
def get_aboniments(request: Request,
                   page: int = Query(1, ge=1),
                   page_size: int = Query(20, le=100),
                   query: str = Query(None)):
    return web_aboniments.get_aboniments(
        page=page,
        page_size=page_size,
        query=query,
        request=request
    )


@router.get('/get/my-aboniments', status_code=200, response_model=List[sc.MyPurchasedAbonimentResponse])
def get_aboniments(request: Request, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_purchased_aboniments(db=db, user=user, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/by-provider/{provider_id}', status_code=200, response_model=sc.ProviderAbonimentsResponse)
def get_provider_aboniments(provider_id: int,
                            request: Request,
                            user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_provider_aboniments(db=db, provider_id=provider_id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                  "error_message": f"{err}"})


@router.get('/get/{aboniment_id}', status_code=200, response_model=sc.AbonimentResponse)
def get_aboniment(request: Request, aboniment_id: int):
    return web_aboniments.get_aboniment(request=request, aboniment_id=aboniment_id)
