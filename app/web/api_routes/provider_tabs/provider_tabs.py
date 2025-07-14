import logging
from fastapi import APIRouter
from app.web.services.provider_tabs import provider_tabs as sv
from app.web.schemas.provider_tabs import provider_tabs as sc
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/tabs", tags=['Provider tabs'],
                   dependencies=[auth()])


@router.get('/get-all/{provider_id}', status_code=200, response_model=sc.ListProviderTabOut)
def get_(provider_id: int):
    return sv.get_all(provider_id=provider_id)


@router.post('/add', status_code=200, response_model=sc.AddedOrDeletedObjectResponse)
def post_api(request: sc.ProviderTabAddRequest):
    return sv.add_provider_tab(request=request)


@router.put('/edit/{id}', status_code=200, response_model=sc.ProviderTabOut)
def post_api(id: int, request: sc.ProviderTabEditRequest):
    return sv.edit_tab(tab_id=id, request=request)


@router.delete("/delete/{id}", response_model=sc.AddedOrDeletedObjectResponse)
def delete_api(id: int):
    return sv.delete_tab(time_id=id)
