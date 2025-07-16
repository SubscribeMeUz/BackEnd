import json
import logging
import requests
from datetime import datetime, timezone
from app.app.redis_client.redis_client import redis_storage
from app.app.schemas.external_services.sms_login_response import SMSTokenResponse, CachedTokenData, SendMessage
from app.config.config import SMS_SERVER, SMS_SERVER_EMAIL, SMS_SERVER_PASSWORD, TOKEN_KEY, TOKEN_EXPIRE


logger = logging.getLogger(__name__)


def get_token_from_cache()->str|None:
    cached = redis_storage.hget(TOKEN_KEY, TOKEN_EXPIRE)
    if cached:
        data = json.loads(cached)
        return data.get('token')
    
    #set_token_in_cache()

def set_token_in_cache(token: str):
    token_date = CachedTokenData(token=token, fetched_at=datetime.now(timezone.utc))
    serilized = json.dumps(token_date.model_dump(),default=str)
    redis_storage.hset(TOKEN_KEY,TOKEN_EXPIRE, serilized)
    redis_storage.expire(TOKEN_KEY, TOKEN_EXPIRE)


def fetch_new_sms_token() -> SMSTokenResponse:
    try:
        response = requests.post(
            SMS_SERVER + "/auth/login",
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data={                      
                "email": SMS_SERVER_EMAIL.strip('""'),
                "password": SMS_SERVER_PASSWORD.strip('""')
            }
            )
        response.raise_for_status()
        json_response = response.json()
        return SMSTokenResponse(**json_response)
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}


def get_valid_token() -> str:
    token = get_token_from_cache()
    if token:
        return token
    new_token = fetch_new_sms_token()
    logger.info(type(new_token), new_token)
    set_token_in_cache(new_token.data.token)
    return new_token.data.token


def sendOTP(phone: str, code: str):
    try:
        otp_form = {
            "message": "Subme.uz sayti ga ro‘yxatdan o‘tish uchun  tasdiqlash kodi " + code,
            "mobile_phone": phone,
            "callback_url": "",
            "from": "4454"      
        }
        logger.info(otp_form)
        response = requests.post(
            SMS_SERVER + "/message/sms/send",
            headers= {"Content-Type": "application/x-www-form-urlencoded",
                     "Authorization" : f"Bearer {get_valid_token()}" },
            data = otp_form
        )
        response.raise_for_status()
        json_response = response.json()
        return json_response
    except requests.exceptions.RequestException as e:
        return {"error": str(e)}
