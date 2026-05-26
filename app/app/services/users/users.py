from fastapi import HTTPException
from sqlalchemy.orm import Session
from app.models.users.users import Users
from app.app.schemas.users import users as sc


def delete_user(db: Session, user_id: int):
    user = db.query(Users).filter(Users.id == user_id).first()
    if not user:
        raise ValueError("User not found")

    if user.phone:
        user.phone = f"deleted_{user.id}_{user.phone}"
    if user.username:
        user.username = f"deleted_{user.id}_{user.username}"

    db.delete(user)
    try:
        db.commit()
        return {"result": "ok"}
    except Exception as err:
        db.rollback()
        raise err


