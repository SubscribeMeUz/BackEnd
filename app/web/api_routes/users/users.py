import logging
from fastapi import APIRouter, HTTPException, Depends, Query, UploadFile, File, Response
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.users import users as sv
from app.app.schemas.users import users as sc


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/users", tags=['Users'])


@router.get('/get/all', status_code=200, response_model=List[sc.UserOut])
def get_all_users(
    user=Depends(auth_handler.auth_wrapper)
):
    try:
        with SessionManager() as db:
            resp = sv.get_all_users(db=db)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/all/users', status_code=200, response_model=sc.UsersListOut)
def get_all_users(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    query: str = Query(None),
    user=Depends(auth_handler.auth_wrapper)
):
    try:
        with SessionManager() as db:
            resp = sv.get_all_users(page=page, page_size=page_size,
                                    string_query=query, db=db)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/{user_id}', status_code=200, response_model=sc.UserOut)
def get_user(user_id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user(db, user_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/by-username/{username}', status_code=200, response_model=sc.UserOut)
def get_user(username: str, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_by_username(db, username)
        return resp
    except Exception as err:
        HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/roles', status_code=200)
def get_roles():
    return [
        sc.UserRoles.ADMIN,
        sc.UserRoles.USER,
        sc.UserRoles.PROVIDER,
        sc.UserRoles.TRAINER,
    ]


@router.put('/change/self', status_code=200)
def change_(request: sc.UserSelfChangeRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            db.add(user)
        resp = sv.user_self_change(db, user, request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.put('/change/{user_id}', status_code=200)
def get_(user_id: int, request: sc.UserChangeRequest, user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.change_user(db, user_id, request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/reset-password/{user_id}', status_code=200)
def get_(user_id, user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.reset_user_password(db, user_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})




# @router.get(, status_code=200)
# def get_(, user: Depends(auth_handler.auth_wrapper)):
#     try:
#         with SessionManager() as db:
#             resp = sv.
#         return resp
#     except Exception as err:
#         raise HTTPException(400, {"title": "error",
#                             "error_message": f"{err}"})
