import random
from sqlalchemy.orm import Session
from fastapi import HTTPException
from app.app.schemas.users import users as sc
from app.web.schemas.users.roles import Roles
from app.models.users.users import Users
from app.models.refresh_token import RefreshToken
from datetime import datetime, date
from app.helpers.auth import auth_handler


def add_user(db: Session, request: sc.OTPPhoneVerifyModel, info: sc.OTPPhoneVerifyModel):
    user = db.query(Users).filter_by(phone=request.phone).first()

    if not user:
        username = info.username
        if not info.username:
            username = 'user_' + ''.join([str(random.randint(0, 9)) for _ in range(5)])
        user = Users(
            phone=request.phone,
            username=username,
            full_name=info.full_name,
            password='',
            role=Roles.user
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    access_token = auth_handler.encode_token(user.username)
    refresh_token, expires = auth_handler.encode_refresh_token(user.id)

    db.add(RefreshToken(user_id=user.id, token=refresh_token, expires=expires))
    db.commit()

    return {
        'access_token': access_token,
        'refresh_token': refresh_token
    }


def refresh_token(db: Session, token: str):
    token_row = db.query(RefreshToken).filter_by(token=token).first()
    if not token_row or token_row.expires < datetime.utcnow():
        raise HTTPException(403, {'detail': 'Refresh token yaroqsiz yoki eskirgan'})

    user = db.query(Users).filter_by(id=token_row.user_id).first()
    if not user:
        raise HTTPException(404, {'detail': 'Foydalanuvchi topilmadi'})

    new_access_token = auth_handler.encode_token(user.username)

    return {'access_token': new_access_token}
