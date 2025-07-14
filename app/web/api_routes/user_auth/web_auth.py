import logging
from fastapi import APIRouter
from app.web.services.user_auth import login as sv
from app.app.schemas.users import users as sc
from app.helpers.auth import admin_auth


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/web/auth", tags=["Web Auth"]
)


@router.post('/login', status_code=200)
def get_token(request: sc.UserLogin):
    logger.info(f"USER with Username: {request.username} requested method get_token")
    return sv.login_user(request)


@router.post('/admin/add-user', status_code=200)
def admin_add_user(request: sc.UserCreate, user=admin_auth()):
    logger.info(f"Admin creating new user {request.username}")
    return sv.create_user(request)
