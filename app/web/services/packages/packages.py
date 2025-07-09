from sqlalchemy.orm import Session
from app.models.packages.packages import AbonimentPackage
from app.models.providers.providers import Providers
from app.web.schemas.packages import packages as sc


def get_all_packages(db: Session, provider_id: int):
    resp = (
        db
        .query(AbonimentPackage)
        .join(AbonimentPackage.provider)
        .filter(Providers.is_deleted == False)
        .filter(AbonimentPackage.provider_id == provider_id,
                AbonimentPackage.is_deleted == False)
        .all()
    )
    return resp


def get_package(db: Session, package_id: int):
    package = (
        db
        .query(AbonimentPackage)
        .join(AbonimentPackage.provider)
        .filter(Providers.is_deleted == False)
        .filter(AbonimentPackage.id == package_id,
                AbonimentPackage.is_deleted == False)
        .first()
    )
    if not package:
        raise ValueError("Not found")
    return package


def add_package(db: Session, request: sc.AbonimentPackageAddRequest):
    package = AbonimentPackage(
        plan_name=request.plan_name,
        label=request.label,
        title=request.title,
        subtitle=request.subtitle,
        count=request.count,
        expiry_days=request.expiry_days,
        discount=request.discount,
        provider_id=request.provider_id
    )
    db.add(package)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}


def edit_package(db: Session, package_id: int, request: sc.AbonimentPackageEditRequest):
    package = get_package(db=db, package_id=package_id)

    for field, value in request.model_dump().items():
        if value is not None:
            setattr(package, field, value)

    db.add(package)
    try:
        db.commit()
        db.refresh(package)
        return package
    except Exception as err:
        db.rollback()
        raise err


def delete_package(db: Session, package_id: int) -> sc.AddedOrDeletedObjectRescponse:
    package = get_package(db=db, package_id=package_id)
    db.delete(package)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}
