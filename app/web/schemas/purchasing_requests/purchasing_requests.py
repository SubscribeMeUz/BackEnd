from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime
from app.app.schemas.purchasing_requests.purchasing_requests import PurchasingRequestsStatuses
from app.app.schemas.users.users import UserOut
from app.app.schemas.aboniments.aboniments import AbonimentsWithPackage


class GetRequestsResponse(BaseModel):
    id: int
    status: PurchasingRequestsStatuses
    purchase_id: Optional[int] = None
    user_id: int
    user: UserOut
    aboniment_id: int
    aboniment: AbonimentsWithPackage
    recorded_date: datetime

    class Config:
        from_attributes = True


ListGetRequestsResponse = List[GetRequestsResponse]
