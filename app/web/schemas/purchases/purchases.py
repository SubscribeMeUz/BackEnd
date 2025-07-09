from pydantic import BaseModel
from typing import Optional, List, Literal
from datetime import datetime, date as date_
from app.web.schemas.aboniments import aboniments
from app.app.schemas.users import users


PurchasesStatusesLiterals = Literal["new", "used"]
class PurchasesStatuses():
    NEW = 'new'
    USED = 'used'


class PurchasePostRequest(BaseModel):
    aboniment_id: int
    user_id: int

    class Config:
        from_attributes = True


class PurchaseFilter(BaseModel):
    date: Optional[date_] = None
    user_id: Optional[int] = None


class PurchaseBase(BaseModel):
    aboniment: aboniments.AbonimentOut
    user: users.UserLessOut
    used_count: int
    status: PurchasesStatusesLiterals


class AddedOrDeletedObjectRescponse(BaseModel):
    result: Literal["Ok", "Failed"]


class PurchaseId(BaseModel):
    id: int


class PurchaseOut(PurchaseBase, PurchaseId):
    class Config:
        from_attributes = True


class PurchaseAdded(AddedOrDeletedObjectRescponse):
    purchase: PurchaseOut

    class Config:
        from_attributes = True


class PurchasesOut(BaseModel):
    total: int
    total_pages: int
    page: int
    page_size: int
    data: List[PurchaseOut]
