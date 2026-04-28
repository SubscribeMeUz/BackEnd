import logging
from fastapi import APIRouter
from app.app.schemas.departments import departments as sc
from app.app.services.departments import departments as sv


logger = logging.getLogger(__name__)
router = APIRouter(prefix="/app/departments", tags=['App Departments'])


@router.get('/get/all', status_code=200, response_model=sc.ListDepartmentsResponse)
def get_all_departments():
    return sv.get_departments()