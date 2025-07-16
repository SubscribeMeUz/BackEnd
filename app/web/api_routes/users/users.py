import logging
from fastapi import APIRouter, Query
from app.web.services.users import users as sv
from app.app.schemas.users import users as sc
from app.helpers.auth import auth, admin_auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/users", tags=['Users'],
                   dependencies=[admin_auth()])


@router.get('/get/all', status_code=200, response_model=sc.ListUserOut)
def get_all_users():
    return sv.get_all_users()


@router.get('/get/all/users', status_code=200, response_model=sc.UsersListOut)
def get_all_users(page: int = Query(1, ge=1),
                  page_size: int = Query(20, le=100),
                  query: str = Query(None)):
    return sv.get_all_users(page=page, page_size=page_size, string_query=query)


@router.get('/get/{user_id}', status_code=200, response_model=sc.UserOut)
def get_user(user_id: int):
    return sv.get_user(user_id=user_id)


@router.get('/get/by-username/{username}', status_code=200, response_model=sc.UserOut)
def get_user(username: str):
    return sv.get_user_by_username(username=username)


@router.get('/roles', status_code=200)
def get_roles():
    return [
        sc.UserRoles.ADMIN,
        sc.UserRoles.USER,
        sc.UserRoles.PROVIDER,
        sc.UserRoles.TRAINER,
    ]


@router.put('/change/self', status_code=200)
def change_user(request: sc.UserSelfChangeRequest, user=auth()):
    return sv.user_self_change(user=user, request=request)


@router.put('/change/{user_id}', status_code=200)
def change_user_password(user_id: int, request: sc.UserChangeRequest):
    return sv.change_user(user_id=user_id, request=request)


@router.get('/reset-password/{user_id}', status_code=200)
def reset_user_password(user_id: int):
    return sv.reset_user_password(user_id=user_id)
