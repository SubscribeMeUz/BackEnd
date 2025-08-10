from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class ActiveSubscriptions(BaseModel):
    provider_id: int


class DailyPurchasesResponse(BaseModel):
    pass


class DailyPurchaseRequest(BaseModel):
    provider_id: Optional[int]
    aboniment_id: Optional[int]

