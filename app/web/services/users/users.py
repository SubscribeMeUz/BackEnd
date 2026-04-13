import math
import logging
from sqlalchemy.orm import Session
from sqlalchemy.sql import or_
from app.models.users.users import Users
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.purchases.purchases import Purchases
from app.app.schemas.users import users as sc
from app.helpers.auth import auth_handler
from app.web.schemas.users.roles import Roles


logger = logging.getLogger(__name__)


def get_all_users(db: Session,
                  page: int = None,
                  page_size: int = None,
                  string_query: str = None,
                  admin: Users = None):
    query = db.query(Users)
    if admin.role != Roles.admin:
        query = query.filter(
            Users.purchases.any(
                Purchases.aboniment.has(
                    Aboniments.provider.has(
                        Providers.owner_id == admin.id
                    )
                )
            )
        )

    if not page:
        return query.all()
    if string_query:
        query = query.filter(
            or_(
                Users.full_name.ilike(f"%{string_query}%"),
                Users.username.ilike(f"%{string_query}%"),
                Users.phone.ilike(f"%{string_query}%")
            )
        )
    offset = (page - 1) * page_size
    total_count = query.count()
    resp = (
        query
        .order_by(Users.id)
        .offset(offset)
        .limit(page_size)
        .all()
        )
    return {
        "total": total_count,
        "total_page": math.ceil(total_count / page_size),
        "page": page,
        "limit": page_size,
        "data": resp
    }


def get_user(db: Session, user_id: int):
    resp = db.query(Users).filter(Users.id == user_id).first()
    if not resp:
        raise ValueError("User not found")
    return resp


def get_user_by_username(db: Session, username: str):
    resp = db.query(Users).filter(Users.username == username).first()
    if not resp:
        raise ValueError("User not found")
    return resp


def change_user(db: Session, user_id: int, request: sc.UserChangeRequest):
    user = db.query(Users).filter(Users.id == user_id).first()
    
    if not user:
        raise ValueError("User not found!")
    if request.username:
        count = db.query(Users).filter(Users.username == request.username,
                                       Users.id != user_id).count()
        if count:
            raise ValueError("This username is already taken")
        user.username = request.username
    if request.new_password:
        user.password = auth_handler.get_password_hash(request.new_password)
    if request.phone:
        user.phone = request.phone
    if request.full_name:
        user.full_name = request.full_name
    if request.role:
        user.role = request.role
    if request.department is not None:
        user.department = request.department
    
    db.add(user)
    try:
        db.commit()
        return {"result": "ok", "user": sc.UserOut.model_validate(user)}
    except Exception as err:
        db.rollback()
        return {"result": "falied", "error": f"{err}"}


def user_self_change(db: Session, user: Users, request: sc.UserSelfChangeRequest):
    if request.username:
        count = db.query(Users).filter(Users.username == request.username,
                                       Users.id != user.id).count()
        if count:
            raise ValueError("This username is already taken")
        user.username = request.username
    if request.password and request.new_password:
        if not auth_handler.verify_password(request.password, user.password):
            raise ValueError("Current password didn't match")
        if request.password == request.new_password:
            raise ValueError("Current password and new password are the same")
        user.password = auth_handler.get_password_hash(request.new_password)
    if request.full_name:
        user.full_name = request.full_name
    if request.department is not None:
        user.department = request.department

    db.add(user)
    try:
        db.commit()
        return {"result": "ok", "user": sc.UserOut.model_validate(user)}
    except Exception as err:
        raise err


def reset_user_password(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise ValueError("User not found")
    user.password = auth_handler.get_password_hash('12345')
    db.add(user)
    try:
        db.commit()
        return {"result": "ok", "message": "The password has reset to 12345"}
    except Exception as err:
        db.rollback()
        return {"result": "failed", "error": err}
