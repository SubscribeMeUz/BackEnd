from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime


class ActiveSubscriptions(BaseModel):
    provider_id: int


class DailyPurchasesResponse(BaseModel):
    pass


class DailyPurchaseRequest(BaseModel):
    provider_id: Optional[int]
    aboniment_id: Optional[int]

class UserAbonimentUseRequest(BaseModel):
    provider_id: int | None = None
    name: str| None = None
    phone: str | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None
    aboniment_id: int | None = None

class UserAbonimentUseResponse(BaseModel):
    user_id: int
    full_name: str
    phone: str
    provider_id: int
    provider_name: str
    aboniment_id: int
    aboniment_name: str
    use_date: datetime
    #quantity_used: int
class PurchaseHistoryRequest(BaseModel):
    from_date: datetime | None = None
    to_date: datetime | None = None
    abonoment_id: int | None = None
    name: str | None = None
    phone: str | None = None
    provider_id: int | None = None


class PurchaseHistoryResponse(BaseModel):
    purchase_id: int
    user_id: int
    user_name: str
    user_phone: str
    provider_id: int
    provider_name: str
    aboniment_id: int
    aboniment_name: str
    purchase_date: datetime
    abonoment_package_name: str
    total_amount: int
    #payment_method: str


class ClientInfoRequest(BaseModel):
    name: str | None = None
    phone: str | None = None
    phone_number: str | None = None
    min_count: int | None = None
    max_count: int | None = None
    from_date: datetime | None = None
    to_date: datetime | None = None

class ClientInfoResponse(BaseModel):
    full_name: str
    user_id: int
    phone_number: str
    purchase_count: int
    last_purchase_date: datetime

class ClientAcceptenceRejectionResponse(BaseModel):
    rejected: int
    accepted: int
    waiting: int


LiteralHoursInterval = Literal["1", "2", "3", "4", "6", "12", "24"]
