import os
import uuid
import math
import shutil
import logging
from passlib.context import CryptContext
from fastapi import HTTPException
from typing import List
from sqlalchemy.orm import Session, Query
from sqlalchemy.sql import func, or_
from app.models.users.users import Users
from app.app.schemas.users import users as sc


logger = logging.getLogger(__name__)


def get_all_users(db: Session,
                  page: int = None,
                  page_size: int = None,
                  string_query: str = None):
    query = db.query(Users)
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
        raise HTTPException(400, {"title": "error",
                                  "error_message": "User not found"})
    return resp


def get_user_by_username(db: Session, username: str):
    resp = db.query(Users).filter(Users.username == username).first()
    if not resp:
        raise HTTPException(400, {"title": "error",
                                  "error_message": "User not found"})
    return resp


def change_user(db: Session, user_id: int, request: sc.UserChangeRequest):
    user = db.query(Users).filter(Users.id == user_id).first()
    
    if not user:
        raise HTTPException(404, "User not found!")
    if request.username:
        count = db.query(Users).filter(Users.username == request.username,
                                       Users.id != user_id).count()
        if count:
            raise HTTPException(400, "This username is already taken")
        user.username = request.username
    if request.password:
        if not check_password(request.password, user.password):
            raise HTTPException(400, "Current password didn't match")
        if request.password == request.new_password:
            raise HTTPException(400, "Current password and new password are the same")
        user.password = get_password_hash(request.new_password)
    if request.phone:
        user.phone = request.phone
    if request.full_name:
        user.full_name = request.full_name
    if request.role:
        user.role = request.role
    
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
            raise HTTPException(400, "This username is already taken")
        user.username = request.username
    if request.password and request.new_password:
        if not check_password(request.password, user.password):
            raise HTTPException(400, "Current password didn't match")
        if request.password == request.new_password:
            raise HTTPException(400, "Current password and new password are the same")
        user.password = get_password_hash(request.new_password)
    if request.full_name:
        user.full_name = request.full_name

    db.add(user)
    try:
        db.commit()
        return {"result": "ok", "user": sc.UserOut.model_validate(user)}
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                  "error_message": f"{err}"})


def reset_user_password(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise HTTPException(404, "User not found")
    user.password = get_password_hash('12345')
    db.add(user)
    try:
        db.commit()
        return {"result": "ok", "message": "The password has reset to 12345"}
    except Exception as err:
        db.rollback()
        return {"result": "failed", "error": err}


def check_password(password: str, user_password_hash: bytes):
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return context.verify(password, user_password_hash)


def get_password_hash(password: str):
    context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    return context.hash(password)


def get_user_for_test(db: Session):
    resp = db.query(Users).all()
    if not resp:
        raise ValueError("Not found")
    return {
        "data": resp
    }
