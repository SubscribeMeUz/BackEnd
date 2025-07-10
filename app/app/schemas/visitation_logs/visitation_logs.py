from pydantic import BaseModel, model_validator
from datetime import datetime, date, time, timedelta
from typing import List, Optional
from app.models.visitation_logs.visitation_logs import VisitationLogs


class VisitationLogTreeOut(BaseModel):
    id: int
    user_id: int
    purchase_id: int
    recorded_date: datetime

    class Config:
        from_attributes = True


class PurchaseTreeOut(BaseModel):
    id: int
    user_id: int
    aboniment_id: int

    visitation_logs: List[VisitationLogTreeOut]

    class Config:
        from_attributes = True


class AbonimentPackageOut(BaseModel):
    id: int
    plan_name: str
    label: str
    title: str
    subtitle: str
    count: int
    expiry_days: int
    discount: int
    provider_id: int


class WorkoutTimeOut(BaseModel):
    id: int
    title: str
    from_time: time
    to_time: time
    discount: int
    provider_id: int


class ProviderTabOut(BaseModel):
    id: int
    label: str
    value: str
    title: str
    provider_id: int


class AbonimentTreeOut(BaseModel):
    id: int
    name: str
    price: int
    aboniment_package: AbonimentPackageOut
    workout_time: WorkoutTimeOut
    provider_tab: ProviderTabOut
    purchases: List[PurchaseTreeOut]

    class Config:
        from_attributes = True


class ProviderTreeOut(BaseModel):
    id: int
    name: str
    location_latt: str
    location_long: str
    logo_url: str
    aboniments: List[AbonimentTreeOut]

    class Config:
        from_attributes = True


class VisitationLogAddRequest(BaseModel):
    provider_id: int
    aboniment_id: int

    class Config:
        from_attribute = True


class UserOut(BaseModel):
    id: int
    username: str
    full_name: str
    phone: str


class ProviderOut(BaseModel):
    id: int
    name: str
    location_latt: str
    location_long: str
    logo_url: str

    class Config:
        from_attributes = True


class AbonimentOut(BaseModel):
    id: int
    name: str
    price: int

    class Config:
        from_attributes = True



class PurchaseOut(BaseModel):
    id: int
    aboniment_id: int
    user_id: int
    recorded_date: datetime

    class Config:
        from_attributes = True


class VisitationLogOut(BaseModel):
    id: int
    user: UserOut
    provider: ProviderOut
    aboniment: AbonimentOut
    purchase: PurchaseOut

    recorded_date: datetime

    @model_validator(mode='before')
    def f(cls, log: VisitationLogs):
        log.provider = log.purchase.aboniment.provider
        log.aboniment = log.purchase.aboniment
        return log

    class Config:
        from_attributes = True


class AddedNewVisitationLog(BaseModel):
    result: str
    log: VisitationLogOut

    class Config:
        from_attributes = True
