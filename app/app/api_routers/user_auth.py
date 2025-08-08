import logging
from fastapi import APIRouter, HTTPException, Body
from app.app.services.user_auth.login import (login_with_otp,
                                          generate_otp, store_otp,
                                          send_sms, verify_otp, clear_storage)
from app.web.services.user_auth.login import create_user 
from app.app.schemas.users import users as sc
from app.app.services.user_auth import user_auth as sv
from app.app.services.external_services.external_api import sendOTP 
from app.app.schemas.external_services.sms_login_response import SendMessage as smsObject
from app.helpers.auth import auth


logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "/user", tags=["Login"]
)


# @router.post('/register/request-otp', status_code=200)
# def request_otp(request: sc.OTPPhoneRegisterRequest):
#     otp_code = generate_otp()
#     store_otp(request, otp_code)

#     send_sms(request.phone, otp_code)

#     return {"title": "success",
#             "message": "OTP sent"}


# @router.post('/register/verify', status_code=200)
# def register_user(request: sc.OTPRegisterRequest,):
#     if not verify_otp(request.phone, request.otp_code):
#         raise HTTPException(status_code=400, detail='Tasdiqlash kodi noto‘g‘ri yoki eskirgan')

#     with SessionManager() as db_session:
#         clear_storage(request.phone)
#         logger.info(f"Verified user: {request.phone}")
#         try:
#             status = create_user(request, db_session)
#             return status
#         except Exception as err:
#             return {"title": "Error",
#                     "error_message": f'{err}'}


# @router.post('/login/request-otp', status_code=200)
# def request_otp(request: sc.OtpPhoneRequest):
#     otp_code = generate_otp()
#     store_otp(request, otp_code)

#     send_sms(request.phone, otp_code)

#     return {"title": "success",
#             "message": "OTP sent"}


# @router.post('/login/verify', status_code=200)
# def login_uuser_with_otp(request: sc.OTPLoginRequest):
#     if not verify_otp(request.phone, request.otp_code):
#         raise HTTPException(status_code=400, detail='Tasdiqlash kodi noto‘g‘ri yoki eskirgan')

#     with SessionManager() as db_session:
#         clear_storage(request.phone)
#         logger.info(f"Verified user: {request.phone}")
#         status = login_with_otp(request.phone, db_session)
#     return status


@router.post('/auth/request-otp')
def request_otp(request: sc.OTPPhoneRegisterRequest):
    code = generate_otp()
    store_otp(request, code)
    #send_sms(request.phone, code)
    #try:
    sendOTP(request.phone, code, request.appsignature)
    return {'status': 'OTP sent'}
    #except Exception as error:
     #   raise HTTPException(status_code=500, detail= str(error))


@router.post('/auth/verify-otp')
def verify_otp_handler(request: sc.AuthVerifyOTPRequest):
    verify = verify_otp(request.phone, request.code)
    if not verify:
        raise HTTPException(400, {'detail': 'Noto‘g‘ri yoki eskirgan kod'})

    return sv.add_user(request=request, info=verify)


@router.post('/auth/refresh')
def refresh_token(request: sc.RefreshTokenRequest = Body(...)):
    if not request.refresh_token:
        raise HTTPException(400, {'detail': 'Refresh token talab qilinadi'})

    return sv.refresh_token(token=request.refresh_token)
