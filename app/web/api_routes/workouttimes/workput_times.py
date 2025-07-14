import logging
from fastapi import APIRouter
from app.web.services.workouttimes import workout_times as sv
from app.web.schemas.workouttimes import workout_times as sc
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/workout-times", tags=['Workout times'],
                   dependencies=[auth()])


@router.get('/get-all/{provider_id}', status_code=200, response_model=sc.ListWorkoutTimeOut)
def get_api(provider_id: int):
    return sv.get_all_workout_times(provider_id=provider_id)


@router.post('/add', status_code=200, response_model=sc.AddedOrDeletedObjectRescponse)
def post_api(request: sc.WorkOutTimeAddRequest):
    return sv.add_workout_time(request=request)


@router.put('/edit/{id}', status_code=200, response_model=sc.WorkoutTimeOut)
def post_api(id: int, request: sc.WorkOutTimeEditRequest):
    return sv.edit_workout_time(time_id=id, request=request)


@router.delete("/delete/{id}", response_model=sc.AddedOrDeletedObjectRescponse)
def delete_api(id: int):
    return sv.delete_workout_time(time_id=id)
