import logging
from sqlalchemy.orm import Session
from app.models.users.users import Users
from app.app.schemas.users import users as sc
from app.helpers.auth import auth_handler


logger = logging.getLogger(__name__)


def login_user(request: sc.UserLogin, db: Session):
    user: Users = db.query(Users).filter(Users.username == request.username).first()

    if isinstance(request, sc.UserLogin):
        if (user is None) or (not auth_handler.verify_password(request.password, user.password)):
            logger.error(f"Invalid username and/or password! {request.username}")
            raise ValueError(detail="Parol yoki Login noto'g'ri yozilgan!")

    logger.info("Access token creating")
    access_token = auth_handler.encode_token(user.username)
    logger.info(f"Successfully Logged in {user.username}:{user.id}")
    return {'token': access_token, 'user': {"id": user.id,
                                            "username" : user.username,
                                            "full_name": user.full_name,
                                            "role": user.role,
                                            "phone": user.phone}}


def create_user(request: sc.UserCreate, db: Session):
    user = db.query(Users).filter(Users.username == request.username).first()
    
    if user is not None:
        logger.error("Username is taken")
        raise ValueError("Username is taken")

    user = db.query(Users).filter(Users.phone == request.phone).first()

    if user is not None:
        logger.error("User phone is taken")
        raise ValueError("Phone number is taken")

    hashed_password = auth_handler.get_password_hash(request.password)

    new_user = Users(username = request.username,
                     password = hashed_password,
                     full_name = request.full_name,
                     phone = request.phone)
    
    if isinstance(request, sc.OTPRegisterRequest):
        new_user.role = sc.UserRoles.USER
    else:
        new_user.role = request.role

    try:
        db.add(new_user)
        db.commit()
    except Exception as err:
        db.rollback()
        raise err

    logger.info(f"User {new_user.username} has been successfully created!")

    user_login = sc.UserLogin(username=new_user.username, password=request.password)

    return {"result": "OK",
            "login": login_user(request=user_login)}
