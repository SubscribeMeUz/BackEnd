from sqlalchemy.orm import Session
from app.models.departments.departments import Departments


def get_departments(db: Session):
    resp = (
        db.query(Departments)
        .filter(Departments.is_deleted == False)
        .order_by(Departments.name)
        .all()
    )
    return resp