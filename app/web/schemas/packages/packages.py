from pydantic import BaseModel
from typing import List, Literal, Optional


class AddedOrDeletedObjectRescponse(BaseModel):
    result: Literal["Ok", "Failed"]


class AbonimentPackageBase(BaseModel):
    plan_name: Optional[str] = None
    label: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    count: int
    expiry_days: int
    discount: int
    provider_id: int


class AbonimentPackageId(BaseModel):
    id: int


class AbonimentPackageAddRequest(AbonimentPackageBase):
    pass


class AbonimentPackageEditRequest(BaseModel):
    plan_name: Optional[str] = None
    label: Optional[str] = None
    title: Optional[str] = None
    subtitle: Optional[str] = None
    count: Optional[int] = None
    discount: Optional[int] = None
    expiry_days: Optional[int] = None


class AbonimentPackageOut(AbonimentPackageBase, AbonimentPackageId):

    class Config:
        from_attributes = True

