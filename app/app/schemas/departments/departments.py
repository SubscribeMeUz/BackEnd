from pydantic import BaseModel
from typing import List


class DepartmentBase(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


ListDepartmentsResponse = List[DepartmentBase]