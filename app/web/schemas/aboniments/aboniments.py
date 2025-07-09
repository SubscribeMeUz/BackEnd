from pydantic import BaseModel, Field
from typing import Optional, List, Dict
from datetime import datetime
from app.app.schemas.users.users import UserOut
from app.web.schemas.packages.packages import AbonimentPackageOut
from app.web.schemas.provider_tabs.provider_tabs import ProviderTabOut
from app.web.schemas.workouttimes.workout_times import WorkoutTimeOut


class ProviderLessOut(BaseModel):
    id: int
    name: str
    owner: UserOut
    logo_url: Optional[str] = ''
    registred_date: datetime

    class Config:
        from_attributes = True


class AbonimentBase(BaseModel):
    name: str
    price: Optional[int] = 0
    provider_id: int
    workout_time_id: int
    provider_tab_id: int
    aboniment_package_id: int


class AbonimentPost(AbonimentBase):
    
    class Config:
        from_attributes = True


class ChangeAboniment(BaseModel):
    name: Optional[str] = None
    price: Optional[int] = None
    workout_time_id: Optional[int] = None
    provider_tab_id: Optional[int] = None
    aboniment_package_id: Optional[int] = None


class AbonimentId(BaseModel):
    id: int


class AbonimentOut(AbonimentBase, AbonimentId):
    provider: ProviderLessOut
    workout_time: WorkoutTimeOut
    provider_tab: ProviderTabOut
    aboniment_package: AbonimentPackageOut

    class Config:
        from_attributes = True


class AbonimentLessOut(AbonimentBase, AbonimentId):

    class Config:
        from_attributes = True


class PaginationParams(BaseModel):
    page: int = Field(1, ge=1)
    page_size: int = Field(20, le=100)


class AbonimentsResponse(BaseModel):
    total: int
    total_pages: int
    page: int
    limit: int
    data: List[AbonimentOut]
