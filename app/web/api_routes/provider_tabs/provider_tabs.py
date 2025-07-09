import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.provider_tabs import provider_tabs as sv
from app.web.schemas.provider_tabs import provider_tabs as sc


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/tabs", tags=['Provider tabs'])


@router.get('/get-all/{provider_id}', status_code=200, response_model=List[sc.ProviderTabOut])
def get_(provider_id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_all(db=db, provider_id=provider_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add', status_code=200, response_model=sc.AddedOrDeletedObjectResponse)
def post_api(request: sc.ProviderTabAddRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_provider_tab(db=db, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.put('/edit/{id}', status_code=200, response_model=sc.ProviderTabOut)
def post_api(id: int, request: sc.ProviderTabEditRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.edit_tab(db=db, tab_id=id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.delete("/delete/{id}", response_model=sc.AddedOrDeletedObjectResponse)
def delete_api(id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.delete_tab(db, time_id=id)
        return resp
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
