from pydantic import BaseModel, model_validator, field_serializer
from typing import Any, Optional, List


class ProvidersLessResponse(BaseModel):
    id: int
    logo: str = ''
    logo_path: str = ''
    name: str = ''
    title: str = ''

    @field_serializer('logo')
    def fpv_logo_url(self, v):
        return self.logo_path

    @field_serializer('title')
    def pv_ttl(self, v):
        return self.name

    class Config:
        from_attributes = True
        validate_by_name = False


ListProvidersLessResponse = List[ProvidersLessResponse]


class PhotosOut(BaseModel):
    path: str = ''
    photo_url: str = ''

    @field_serializer('photo_url')
    def photos_url_(self, v):
        return self.path

    class Config:
        from_attributes = True
        populate_by_name = True


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
