from pydantic import BaseModel
from typing import Literal, Optional, List
from datetime import time


class WorkOutTimeBase(BaseModel):
    title: str
    from_time: time
    to_time: time
    discount: int
    provider_id: int


class WorkOutTimeId(BaseModel):
    id: int


class WorkOutTimeAddRequest(WorkOutTimeBase):
    pass


class WorkOutTimeEditRequest(WorkOutTimeBase):
    title: str
    from_time: Optional[time] = None
    to_time: Optional[time] = None
    discount: Optional[int] = None


class WorkoutTimeOut(WorkOutTimeBase, WorkOutTimeId):

    class Config:
        from_attributes = True


ListWorkoutTimeOut = List[WorkoutTimeOut]


class AddedOrDeletedObjectRescponse(BaseModel):
    result: Literal["Ok", "Failed"]
