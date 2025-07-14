from pydantic import BaseModel, Field, model_validator
from typing import Any, Optional, List
from app.models.providers.providers import Providers


class ProvidersLessResponse(BaseModel):
    id: int
    logo: str
    name: str
    title: str = Field(..., alias='name')

    class Config:
        from_attributes = True
        validate_by_name = True


class PhotosOut(BaseModel):
    photo_url: str


class ProviderDetailResponse(ProvidersLessResponse):
    location_latt: str
    location_long: str
    location_name: Optional[str] = ''
    discounts: List
    packages: list
    necessary_tools: Optional[str]
    about_description: Optional[str]
    photos: List[PhotosOut]

    @model_validator(mode='before')
    def f(cls, data: Any):
        data.discounts = sorted([i.discount for i in data.aboniment_packages])
        data.packages = sorted([i.count for i in data.aboniment_packages if i.discount != 100])
        return data

    class Config:
        from_attributes = True
