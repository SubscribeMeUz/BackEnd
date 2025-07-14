import logging
from fastapi import APIRouter
from app.app.schemas.users import users as sc
from app.app.services.users import users as sv
from app.web.services.users import users as web_sv
from app.helpers.auth import auth


router = APIRouter(prefix="/user", tags=['User menu'])
logger = logging.getLogger(__name__)


@router.get('/get-me', status_code=200, response_model=sc.UserOut)
def get_api(user=auth()):
    return user


@router.put('/self-change', status_code=200)
def get_(request: sc.UserSelfChangeRequest, user=auth()):
    return web_sv.user_self_change(user=user, request=request)
