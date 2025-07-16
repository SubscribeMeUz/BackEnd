from pydantic import BaseModel, Field
from datetime import datetime
from dataclasses import dataclass

class TokenData(BaseModel):
    token: str

class SMSTokenResponse(BaseModel):
    message: str
    data : TokenData
    token_type: str

    class Config:
        from_attribute = True


class CachedTokenData(BaseModel):
    token:str
    fetched_at: datetime

class SendMessage(BaseModel):
    mobile_phone: str
    message: str
    from_: str = Field(..., alias="from")
    callback_url: str