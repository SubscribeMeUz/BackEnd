import logging
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Response, Query, Request
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.app.schemas.providers import providers as sc
from app.app.services.providers import providers as sv

from app.web.api_routes.providers import providers as web_providers


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/app/providers", tags=['App Providers'])


@router.get('/get/all', status_code=200, response_model=List[sc.ProvidersLessResponse])
def get_all_providers(request: Request, query: str = Query(None)):
    try:
        with SessionManager() as db:
           resp = sv.get_providers(db=db, query=query, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                  "error_message": f"{err}"})


# @router.get('/get/my-subcriptions', status_code=200, response_model=List[sc.ProviderOut])
# def get_user_providers(request: Request, user=Depends(auth_handler.auth_wrapper)):
#     try:
#         with SessionManager() as db:
#            resp = sv.
#         return resp
#     except Exception as err:
#         raise HTTPException(400, {"title": "error",
#                                   "error_message": f"{err}"})


# @router.get('/get/by-owner/{owner_id}', status_code=200, response_model=List[sc.ProviderOut])
# def get_providers_by_owner(owner_id: int,
#                            request: Request,
#                            user=Depends(auth_handler.auth_wrapper)):
#     return web_providers.get_providers_by_owner(
#         owner_id=owner_id,
#         user=user,
#         request=request
#     )


@router.get('/get/{provider_id}', status_code=200, response_model=sc.ProviderDetailResponse)
def get_provider(provider_id: int,
                 request: Request):
    try:
        with SessionManager() as db:
            resp = sv.get_provider(db=db, provider_id=provider_id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                  "error_message": f"{err}"})


# @router.get(, status_code=200)
# def get_(, user=Depends(auth_handler.auth_wrapper)):
#     try:
#         with SessionManager() as db:
#             resp = sv.
#         return resp
#     except Exception as err:
#         raise HTTPException(400, {"title": "error",
#                             "error_message": f"{err}"})
