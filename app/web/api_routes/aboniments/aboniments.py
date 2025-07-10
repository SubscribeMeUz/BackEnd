import logging
from fastapi import APIRouter, HTTPException, Depends, Query, Request
from fastapi.responses import FileResponse
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.aboniments import aboniments as sv
from app.web.schemas.aboniments import aboniments as sc


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/aboniments", tags=['Aboniments'])


@router.get('/get/all', status_code=200, response_model=sc.AbonimentsResponse)
def get_aboniments(request: Request,
                   page: int = Query(1, ge=1),
                   page_size: int = Query(20, le=100),
                   query: str = Query(None)):
    try:
        with SessionManager() as db:
            resp = sv.get_aboniments(db=db, page=page,
                                     page_size=page_size,
                                     query=query,
                                     request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/related-by-user', status_code=200, response_model=sc.AbonimentsResponse)
def get_aboniments_related_by_user(page: int = Query(1, ge=1),
                                   page_size: int = Query(20, le=100),
                                   user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_aboniments_related_by_user(db, user, page, page_size)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/by-provider/{provider_id}', status_code=200, response_model=List[sc.AbonimentOut])
def get_provider_aboniments(request: Request,
                            provider_id: int,
                            user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_provider_aboniments(db, provider_id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/{aboniment_id}', status_code=200, response_model=sc.AbonimentOut)
def get_aboniment(request: Request, aboniment_id: int):
    try:
        with SessionManager() as db:
            resp = sv.get_aboniment(db, aboniment_id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add', status_code=200)
def add_aboniment(request: sc.AbonimentPost, user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_aboniment(db, request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.put('/change/{aboniment_id}', status_code=200)
def change_aboinment(aboniment_id: int, request: sc.ChangeAboniment,
                     base_request: Request,
                     user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.change_aboniment(db, aboniment_id, request, base_request=base_request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.delete('/delete/{aboniment_id}', status_code=200)
def delete_aboniment(aboniment_id: int, user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.delete_aboniment(db, aboniment_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/qr-code/{aboniment_id}', status_code=200)
def get_api(aboniment_id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.generate_qr_code(db=db, aboniment_id=aboniment_id)
        return FileResponse(resp)
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/qr-code-by-provider/{provider_id}', status_code=200)
def get_api(provider_id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.generate_qr_code(db=db, provider_id=provider_id)
        return FileResponse(resp)
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


# @router.get(, status_code=200)
# def get_(, user: Depends(auth_handler.auth_wrapper)):
#     try:
#         with SessionManager() as db:
#             resp = sv.
#         return resp
#     except Exception as err:
#         raise HTTPException(400, {"title": "error",
                            # "error_message": f"{err}"})
