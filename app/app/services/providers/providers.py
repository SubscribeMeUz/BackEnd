from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.photos.photos import Photos


def get_providers(db: Session, query: str):
    resp = db.query(Providers)
    if query:
        resp = (
            resp
            .filter(or_(
                Providers.name.ilike(f"%{query}%")
            ), Providers.is_deleted == False)
        )
    resp = (
        resp
        .order_by(Providers.name)
        .all()
    )
    return resp


def get_provider(db: Session, provider_id: int):
    resp = (
        db
        .query(Providers)
        .options(joinedload(Providers.aboniment_packages),
                 joinedload(Providers.photos))
        .filter(Providers.id == provider_id,
                Providers.is_deleted == False)
        .first()
    )
    if not resp:
        raise ValueError("Not found!")
    return resp
