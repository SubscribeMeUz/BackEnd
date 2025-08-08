from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime
from fastapi import HTTPException
from typing import Optional, List
from enum import Enum


class UserRoles(str, Enum):
    USER = 'user'
    PROVIDER = 'provider'
    TRAINER = 'trainer'
    ADMIN = 'admin'


class UserCreate(BaseModel):
    username: str
    password: str
    phone: str
    full_name: str
    role: UserRoles

    @field_validator('phone')
    def validate_phone(cls, v):
        digits = ''.join(filter(str.isdigit, v))

        if len(digits) == 9:
            return '+998' + digits
        elif len(digits) == 12 and digits.startswith('998'):
            return '+' + digits
        else:
            raise HTTPException(400, {"title": "error",
                                "error_message": "Telefon raqam noto‘g‘ri formatda. To‘g‘ri format: +998XXXXXXXXX"})

    class Config:
        from_attributes = True


class OTPRegisterRequest(BaseModel):
    phone: str
    otp_code: str
    username: str
    password: str
    phone: str
    full_name: str

    class Config:
        from_attributes = True


class OtpPhoneRequest(BaseModel):
    phone: str

    @field_validator('phone')
    def validate_phone(cls, v):
        digits = ''.join(filter(str.isdigit, v))

        if len(digits) == 9:
            return '+998' + digits
        elif len(digits) == 12 and digits.startswith('998'):
            return '+' + digits
        else:
            raise HTTPException(400, {"title": "error",
                                "error_message": "Telefon raqam noto‘g‘ri formatda. To‘g‘ri format: +998XXXXXXXXX"})

    class Config:
        from_attributes = True


class OTPPhoneRegisterRequest(OtpPhoneRequest):
    username: str = ''
    full_name: str = ''
    appsignature: str = 'sign'
    
    class Config:
        from_attributes = True        


class AuthVerifyOTPRequest(OtpPhoneRequest):
    code: str


class OTPPhoneVerifyModel(OTPPhoneRegisterRequest):
    username: Optional[str] = None
    full_name: Optional[str] = None
    phone: str
    code: str
    expires: datetime


class OTPLoginRequest(BaseModel):
    phone: str
    otp_code: str


class RefreshTokenRequest(BaseModel):
    refresh_token: str


class UserLogin(BaseModel):
    username: str
    password: str

    class Config:
        from_attributes = True
        

class User(BaseModel):
    username: str
    full_name: str

    class Config:
        from_attributes = True


class UserChangeRequest(BaseModel):
    username: Optional[str] = None
    new_password: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None
    role: Optional[str] = None


class UserSelfChangeRequest(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    new_password: Optional[str] = None
    phone: Optional[str] = None
    full_name: Optional[str] = None


class UserOut(BaseModel):
    id: int
    username: str
    phone: str
    full_name: str
    role: str

    class Config:
        from_attributes = True


ListUserOut = List[UserOut]


class UserLessOut(BaseModel):
    id: int
    username: str
    phone: str
    full_name: str

    class Config:
        from_attributes = True


class UsersListOut(BaseModel):
    total: int
    total_page: int
    page: int
    limit: int
    data: List[UserOut]


class UserTestResponse(BaseModel):
    full_detail: Optional[str] = None

    @model_validator(mode='before')
    def get_full(cls, user):
        user.full_detail = f"{user.id} - {user.username} | {user.full_name}"

        return user

    class Config:
        from_attributes = True


class UserTestResponses(BaseModel):
    data: List[UserTestResponse]

    class Config:
        from_attributes = True
