import logging
from fastapi import APIRouter, UploadFile, File, Depends, Form, HTTPException
from app.middleware.auth import AuthHandler
from app.web.services.user_auth.login import login_user, create_user
from app.db.database import SessionManager
from app.app.schemas.users.users import UserLogin, UserCreate, OTPRegisterRequest, OTPLoginRequest


auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/web/auth", tags=["Web Auth"]
)


@router.post('/login', status_code=200)
def get_token(request: UserLogin):
    with SessionManager() as db:
        logger.info(f"USER with Username: {request.username} requested method get_token")
        status = login_user(request, db)
    return status


@router.post('/admin/add-user', status_code=200)
def admin_add_user(request: UserCreate, user=Depends(admin_auth_handler.auth_wrapper)):
    with SessionManager() as db:
        logger.info(f"Admin creating new user {request.username}")
        resp = create_user(request, db)
    return resp
