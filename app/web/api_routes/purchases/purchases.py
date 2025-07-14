import logging
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Response, Query, Request
from typing import Optional
from datetime import datetime, date
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.purchases import purchases as sv
from app.web.schemas.purchases import purchases as sc


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/purchases", tags=['Purchases'])


@router.get('/get', status_code=200, response_model=sc.PurchasesOut)
def get_purchases(
    request: Request,
    aboniment_id: Optional[int] = Query(None),
    user_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    date_filter: Optional[date] = Query(None),
    user=Depends(auth_handler.auth_wrapper)
):
    try:
        with SessionManager() as db:
            resp = sv.get_filtered_purchases(
                db=db,
                request=request,
                aboniment_id=aboniment_id,
                page=page,
                page_size=page_size,
                date=date_filter,
                user_id=user_id
            )
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/user-purchases', status_code=200, response_model=sc.PurchasesOut)
def get_user_purchases(request: Request,
                       page: int = Query(1, ge=1),
                       page_size: int = Query(20, le=100),
                       date_filter: Optional[date] = Query(None),
                       user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_purchases(db=db,
                                         request=request,
                                         user=user,
                                         page=page,
                                         page_size=page_size,
                                         date=date_filter)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add', status_code=200, response_model=sc.PurchaseAdded)
def add_purchase(request: sc.PurchasePostRequest, base_request: Request,
                 user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_purchase(db, request, base_request=base_request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


# @router.get(, status_code=200)
# def get_(, user: Depends(auth_handler.auth_wrapper)):
#    try:
#        with SessionManager() as db:
#            resp = sv.
#        return resp
#    except Exception as err:
#        raise HTTPException(400, {"title": "error",
#                            "error_message": f"{err}"})
