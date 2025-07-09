import requests
import random
import logging
from fastapi import HTTPException
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from app.config import config
from app.db.database import SessionLocal
from app.middleware.auth import AuthHandler
from app.models.users.users import Users
from app.app.schemas.users import users as sc
from app.app.redis_client.redis_client import redis_storage


logger = logging.getLogger(__name__)

auth_handler = AuthHandler()


def login_with_otp(phone: str, db: Session):
    user: Users = db.query(Users).filter(Users.phone == phone.strip()).first()

    if not user:
        return {
            "title": "error",
            "error_message": "User not found error"
        }
    
    logger.info("Access token creating")
    access_token = auth_handler.encode_token(user.username)
    logger.info(f"Successfully Logged in {user.username}:{user.id}")
    return { 'token': access_token, 'user': {"id": user.id,
                                             "username" : user.username,
                                             "full_name": user.full_name,
                                             "role": user.role,
                                             "phone": user.phone}}


def generate_otp():
    return str(random.randint(10000, 99999))


def store_otp(request: sc.OTPPhoneRegisterRequest, code: str):
    redis_storage.delete(request.phone)
    exp = (datetime.utcnow() + timedelta(minutes=5)).timestamp()
    redis_storage.hset(request.phone,
                       mapping=sc.OTPPhoneVerifyModel(
                           **request.model_dump(),
                           code=code,
                           expires=exp)
                           .model_dump(mode='json'))


def verify_otp(phone: str, code: str) -> bool:
    try:
        raw_data = redis_storage.hgetall(phone)
        data = {k.decode(): v.decode() for k, v in raw_data.items()}
        info = sc.OTPPhoneVerifyModel(**data)
        if not info:
            return False
        if datetime.utcnow().timestamp() > info.expires.timestamp():
            return False
        if not info.code == code:
            return False
        return info
    
    except Exception as err:
        logger.error(err)
        raise HTTPException(400, {
            "title": "error",
            "error_message": f'{err}'
        })


def clear_storage(phone: str):
    redis_storage.delete(phone)


def send_sms(phone: str, code: str):
    print(f"Sending OTP {code} to {phone}")
    logger.info(f"Sending OTP {code} to {phone}")

    json_body = {
        'phone_number': phone,
        'code_length': 5,
        'ttl': 60,
        'payload': code,
    }
    resp = post_request_status(json_body)
    logger.info(f'OTP response: {resp}')
    return {
        'result': "Ok",
        'message': "OTP sent"
    }


def post_request_status(json_body):
    HEADERS = {
        'Authorization': f'Bearer {config.TELEGRAM_OTP_TOKEN}',
        'Content-Type': 'application/json'
    }
    TELEGRAM_OTP_URL = 'https://gatewayapi.telegram.org/sendVerificationMessage'

    resp = requests.post(TELEGRAM_OTP_URL, headers=HEADERS, json=json_body)
    if resp.ok:
        return resp.json()
    else:
        logger.error(f'OTP error: {resp.text}')
        raise HTTPException(400, f"Error: {resp.text}")
