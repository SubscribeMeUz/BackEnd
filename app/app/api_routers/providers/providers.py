import logging
from fastapi import APIRouter, Query
from app.app.schemas.providers import providers as sc
from app.app.services.providers import providers as sv
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/app/providers", tags=['App Providers'])


@router.get('/get/all', status_code=200, response_model=sc.ListProvidersLessResponse)
def get_all_providers(query: str = Query(None)):
    return sv.get_providers(query=query)


@router.get('/get/{provider_id}', status_code=200, response_model=sc.ProviderDetailResponse)
def get_provider(provider_id: int):
    return sv.get_provider(provider_id=provider_id)


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
