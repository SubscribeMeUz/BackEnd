from pydantic import BaseModel
from datetime import datetime
from typing import Literal
from app.app.schemas.aboniments import aboniments as ab_sc


PurchasingRequestsStatuses = Literal['new', 'accessed', 'denied']

class PurchasingRequestsStatus:
    NEW = 'new'
    ACCESSED = 'accessed'
    DENIED = 'denied'


class PurchasingRequestAdd(BaseModel):
    aboniment_id: int


class UserRequests(BaseModel):
    id: int
    user_id: int
    aboniment_id: int
    recorded_date: datetime
    status: PurchasingRequestsStatuses
    aboniment: ab_sc.AbonimentsWithPackage
