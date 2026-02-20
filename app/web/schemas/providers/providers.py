import json
from typing import List, Optional, Any
from pydantic import BaseModel, model_validator
from app.app.schemas.users.users import UserOut
from app.web.schemas.aboniments.aboniments import AbonimentLessOut
from app.web.schemas.packages.packages import AbonimentPackageOut
from app.web.schemas.provider_tabs.provider_tabs import ProviderTabOut
from app.web.schemas.workouttimes.workout_times import WorkoutTimeOut
from app.app.services.tools.tools import TOOLS
from datetime import datetime, time


TOOLS_BY_ID = {t["id"]: t for t in TOOLS}


class ProviderBase(BaseModel):
    name: str
    location_latt: str
    location_long: str
    tools: List[dict] = []
    logo_path: str = ''
    rules_description: Optional[str] = None

    owner: UserOut
    registred_date: datetime

    @model_validator(mode='before')
    def resolve_tools(cls, data: Any):
        try:
            tool_ids = json.loads(data.necessary_tools or '[]')
            data.tools = [TOOLS_BY_ID[i] for i in tool_ids if i in TOOLS_BY_ID]
        except Exception:
            data.tools = []
        return data

    class Config:
        from_attributes = True


class ProviderId(BaseModel):
    id: int


class ProviderOut(ProviderBase, ProviderId):

    class Config:
        from_attributes = True


ListProviderOut = List[ProviderOut]


class ProvidersAllOut(BaseModel):
    total: int
    page: int
    total_page: int
    limit: int
    data: List[ProviderOut]


class PhotosOut(BaseModel):
    id: int
    path: str = ''


class ProviderDetailResponse(ProviderBase):
    name: str
    pic_hours: List[time]
    rules_description: Optional[str] = None
    location_latt: str
    location_long: str
    location_name: Optional[str] = ''
    logo_path: str = ''

    owner: UserOut
    aboniments: List[AbonimentLessOut]
    aboniment_packages: List[AbonimentPackageOut]
    workout_times: List[WorkoutTimeOut]
    provider_tabs: List[ProviderTabOut]
    photos: List[PhotosOut]

    registred_date: datetime

    class Config:
        from_attributes = True


class ProviderAddedResponse(BaseModel):
    result: str
    provider: Optional[ProviderOut] = None
    error: Optional[str] = None
