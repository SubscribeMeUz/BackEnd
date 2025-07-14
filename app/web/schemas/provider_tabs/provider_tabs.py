from pydantic import BaseModel
from typing import Literal, Optional, List


class ProviderTabBase(BaseModel):
    label: str
    value: str
    title: str
    provider_id: int


class ProviderBaseId(BaseModel):
    id: int


class ProviderTabAddRequest(ProviderTabBase):

    class Config:
        from_attributes = True


class ProviderTabEditRequest(BaseModel):
    label: Optional[str] = None
    value: Optional[str] = None
    title: Optional[str] = None


class ProviderTabOut(ProviderTabBase, ProviderBaseId):

    class Config:
        from_attributes = True


ListProviderTabOut = List[ProviderTabOut]


class AddedOrDeletedObjectResponse(BaseModel):
    result: Literal["Ok", "Failed"]
