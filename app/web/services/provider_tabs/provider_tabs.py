import logging
from sqlalchemy.orm import Session
from app.web.schemas.provider_tabs import provider_tabs as sc
from app.models.provider_tabs.provider_tabs import ProviderTabs


logger = logging.getLogger(__name__)


def get_all(db: Session, provider_id: int):
    resp = db.query(ProviderTabs).filter(ProviderTabs.provider_id == provider_id).all()
    return resp


def _get_tab(db: Session, tab_id: int):
    tab: ProviderTabs = db.query(ProviderTabs).filter(ProviderTabs.id == tab_id).first()
    if not tab:
        raise ValueError("Not found")
    return tab


def get_tab(db: Session, tab_id: int):
    return _get_tab(db=db, tab_id=tab_id)


def add_provider_tab(db: Session, request: sc.ProviderTabAddRequest):
    tab = ProviderTabs(
        label = request.label,
        value = request.value,
        title = request.title,
        provider_id = request.provider_id
    )
    db.add(tab)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}


def edit_tab(db: Session, tab_id: int, request: sc.ProviderTabEditRequest):
    tab = _get_tab(db=db, tab_id=tab_id)
    
    for field, value in request.model_dump().items():
        if value is not None:
            setattr(tab, field, value)

    db.add(tab)
    try:
        db.commit()
        db.refresh(tab)
        return tab
    except Exception as err:
        db.rollback()
        raise err


def delete_tab(db: Session, tab_id: int) -> sc.AddedOrDeletedObjectResponse:
    tab = _get_tab(db=db, tab_id=tab_id)
    db.delete(tab)
    try:
        db.commit()
    except Exception as err:
        db.rollback()
        raise err
    return {"result": "Ok"}
