import logging
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Response, Query, Request
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.app.schemas.users import users as sc
from app.app.services.users import users as sv
from app.web.services.users import users as web_sv


router = APIRouter(prefix="/user", tags=['User menu'])
auth_handler = AuthHandler()


@router.get('/get-me', status_code=200, response_model=sc.UserOut)
def get_api(user=Depends(auth_handler.auth_wrapper)):
    try:
        return user
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.put('/self-change', status_code=200)
def get_(request: sc.UserSelfChangeRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = web_sv.user_self_change(db=db, user=user, request=request)
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
