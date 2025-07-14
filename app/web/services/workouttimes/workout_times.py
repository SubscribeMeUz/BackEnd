from sqlalchemy.orm import Session
from app.models.workouttimes.workout_times import WorkOutTimes
from app.web.schemas.workouttimes import workout_times as sc


def get_all_workout_times(db: Session, provider_id: int):
    resp = db.query(WorkOutTimes).filter(WorkOutTimes.provider_id == provider_id).all()
    return resp


def get_workout_time(db: Session, time_id: int) -> WorkOutTimes:
    wk_time = db.query(WorkOutTimes).filter(WorkOutTimes.id == time_id).first()
    if not wk_time:
        raise ValueError("Not found!")
    return wk_time


def add_workout_time(db: Session, request: sc.WorkOutTimeAddRequest):
    wk_time = WorkOutTimes(
        title=request.title,
        from_time=request.from_time,
        to_time=request.to_time,
        discount=request.discount,
        provider_id=request.provider_id
    )
    db.add(wk_time)
    try:
        db.commit()
        db.refresh(wk_time)
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}


def edit_workout_time(db: Session, time_id: int, request: sc.WorkOutTimeEditRequest):
    wk_time = get_workout_time(time_id=time_id)
    for field, value in request.model_dump().items():
        if value is not None:
            setattr(wk_time, field, value)
    db.add(wk_time)
    try:
        db.commit()
        db.refresh(wk_time)
        return wk_time
    except Exception as err:
        db.rollback()
        raise err


def delete_workout_time(db: Session, time_id: int) -> sc.AddedOrDeletedObjectRescponse:
    wk_time = get_workout_time(time_id=time_id)
    db.delete(wk_time)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}
