from sqlalchemy.orm import Session, joinedload
from sqlalchemy import or_
from typing import List
from urllib.parse import urljoin
from fastapi import Request
from app.models.providers.providers import Providers
from app.models.aboniments.aboniments import Aboniments
from app.models.provider_tabs.provider_tabs import ProviderTabs
from app.models.workouttimes.workout_times import WorkOutTimes
from app.models.photos.photos import Photos


def add_logo_url(resp: List[Providers], request: Request):
    if resp is None:
        return
    q = False
    if isinstance(resp, Providers):
        q = True
        resp = [resp]
    for pr in resp:
        setattr(pr, 'logo', urljoin(request.base_url.__str__(), pr.logo_path))
        if pr.photos:
            for photo in pr.photos:
                assert isinstance(photo, Photos)
                setattr(photo, 'photo_url', urljoin(request.base_url.__str__(), photo.path))
    if q:
        return resp[0]
    return resp


def get_providers(db: Session, query: str, request: Request):
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
    return add_logo_url(resp, request)


def get_provider(db: Session, provider_id: int, request: Request):
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
    return add_logo_url(resp, request)
