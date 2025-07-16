import logging
from fastapi import APIRouter, Query
from fastapi.responses import FileResponse
from app.web.services.aboniments import aboniments as sv
from app.web.schemas.aboniments import aboniments as sc
from app.helpers.auth import provider_auth, admin_auth, auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/aboniments", tags=['Aboniments'],
                   dependencies=[provider_auth()])


@router.get('/get/all', status_code=200, response_model=sc.AbonimentsResponse)
def get_aboniments(page: int = Query(1, ge=1),
                   page_size: int = Query(20, le=100),
                   query: str = Query(None),
                   owner = provider_auth()):
    return sv.get_aboniments(page=page,
                             page_size=page_size,
                             query=query,
                             owner=owner)


@router.get('/get/related-by-user', status_code=200, response_model=sc.AbonimentsResponse)
def get_aboniments_related_by_user(page: int = Query(1, ge=1),
                                   page_size: int = Query(20, le=100),
                                   user=auth()):
    return sv.get_aboniments_related_by_user(user=user, page=page, page_size=page_size)


@router.get('/get/by-provider/{provider_id}', status_code=200, response_model=sc.ListAbonimentOut)
def get_provider_aboniments(provider_id: int, _=provider_auth()):
    return sv.get_provider_aboniments(provider_id=provider_id)


@router.get('/get/{aboniment_id}', status_code=200, response_model=sc.AbonimentOut)
def get_aboniment(aboniment_id: int, owner=provider_auth()):
    return sv.get_aboniment(aboniment_id=aboniment_id, owner=owner)


@router.post('/add', status_code=200)
def add_aboniment(request: sc.AbonimentPost, _=admin_auth()):
    return sv.add_aboniment(request=request)


@router.put('/change/{aboniment_id}', status_code=200)
def change_aboinment(aboniment_id: int, request: sc.ChangeAboniment, owner=provider_auth()):
    return sv.change_aboniment(aboniment_id=aboniment_id, request=request, owner=owner)


@router.delete('/delete/{aboniment_id}', status_code=200)
def delete_aboniment(aboniment_id: int, _=admin_auth()):
    return sv.delete_aboniment(aboniment_id=aboniment_id)


@router.get('/qr-code/{aboniment_id}', status_code=200)
def get_api(aboniment_id: int):
    return FileResponse(
        sv.generate_qr_code(aboniment_id=aboniment_id)
    )


@router.get('/qr-code-by-provider/{provider_id}', status_code=200)
def get_api(provider_id: int):
    return FileResponse(
        sv.generate_qr_code(provider_id=provider_id)
    )
