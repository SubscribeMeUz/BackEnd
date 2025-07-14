import logging
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Response, Query, Request
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.app.schemas.purchasing_requests import purchasing_requests as sc
from app.app.services.purchasing_requests import purchasing_requests as sv


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/purchasing-requests', tags=['App Purchasing requests'])
auth_handler = AuthHandler()


@router.post('/add', status_code=200)
def post_api(request: sc.PurchasingRequestAdd, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_purchasing_request(db=db, request=request, user=user)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get-my-requests', status_code=200, response_model=List[sc.UserRequests])
def get_(user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_requests(db=db, user=user)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


# @router.get(, status_code=200)
# def get_(, user=Depends(auth_handler.auth_wrapper)):
#     try:
#         with SessionManager() as db:
#             resp = sv.
#         return resp
#     except Exception as err:
#         raise HTTPException(400, {"title": "error",
#                             "error_message": f"{err}"})
