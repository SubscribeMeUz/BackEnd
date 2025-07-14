import logging
from fastapi import APIRouter, Request, HTTPException, Depends, Form, UploadFile, File, Response, Query
from typing import List
from app.web.schemas.providers import providers as sc
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.providers import providers as sv


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/providers", tags=['Providers'])


@router.get('/get/all', status_code=200, response_model=List[sc.ProviderOut])
def get_all_providers(request: Request):
    try:
        with SessionManager() as db:
            resp = sv.get_all_providers(db, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                "error_message": f"{err}"})


@router.get('/get/all/providers', status_code=200, response_model=sc.ProvidersAllOut)
def get_providers_with_pagination(
    request: Request,
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    query: str = Query(None),
):
    try:
        with SessionManager() as db:
            resp = sv.get_all_providers_with_filters(
                request=request,
                db=db,
                page=page,
                page_size=page_size,
                string_query=query)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/related-by-user', status_code=200, response_model=List[sc.ProviderOut])
def get_my_subcriptions(request: Request, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_providers_related_by_user(db, user, request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/by-owner/{owner_id}', status_code=200, response_model=List[sc.ProviderOut])
def get_providers_by_owner(request: Request,
                           owner_id: int,
                           user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_providers_by_owner(db, owner_id, request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/get/{provider_id}', status_code=200, response_model=sc.ProviderDetailResponse)
def get_provider(request: Request, provider_id: int):
    try:
        with SessionManager() as db:
            resp = sv.get_provider(request, db, provider_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                    "error_message": f"{err}"})


@router.post('/add', status_code=200, response_model=sc.ProviderAddedResponse)
def add_provider(request: Request,
                 name: str = Form(...),
                 location_latt: str = Form(...),
                 location_long: str = Form(...),
                 necessary_tools: str = Form(''),
                 about_description: str = Form(None),
                 logo: UploadFile = File(...),
                 owner_id: int = Form(...),
                 user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            logo_path = sv.save_file(logo)
            status_code, resp = sv.add_provider(
                db=db,
                request=request,
                name=name,
                location_latt=location_latt,
                location_long=location_long,
                necessary_tools=necessary_tools,
                about_description=about_description,
                logo_path=logo_path,
                owner_id=owner_id
            )
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                        "error_message": f"{err}"})


@router.put('/edit/{provider_id}', status_code=200)
def edit_provider(provider_id: int,
                  name: str = Form(None),
                  location_latt: str = Form(None),
                  location_long: str = Form(None),
                  about_description: str = Form(None),
                  logo: UploadFile = File(None),
                  owner_id: int = Form(None),
                  user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            logo_path = sv.save_file(logo)
            resp = sv.edit_provider(
                db=db,
                provider_id=provider_id,
                name=name,
                location_latt=location_latt,
                location_long=location_long,
                about_description=about_description,
                logo_path=logo_path,
                owner_id=owner_id
            )
        if isinstance(resp, bool) and resp:
            return Response(status_code=200, content='Edited!')
        else:
            HTTPException(400, resp)
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                        "error_message": f"{err}"})


@router.delete('/delete/{provider_id}')
def delete_provider(provider_id: int, user=Depends(admin_auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.delete_provider(db, provider_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add-photo/{provider_id}', status_code=200)
def post_api(request: Request,
             provider_id: int,
             file: UploadFile,
             user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            path = sv.save_file(file=file)
            resp = sv.save_provider_photo(request=request, db=db, provider_id=provider_id, photo=path)    
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.delete('/delete-photo/{photo_id}', status_code=200)
def delete_api(photo_id: int, user=Depends(auth_handler.auth_wrapper)):
   try:
       with SessionManager() as db:
           resp = sv.delete_photo(db=db, photo_id=photo_id)
       return resp
   except Exception as err:
       raise HTTPException(400, {"title": "error",
                           "error_message": f"{err}"})


# @router.get(, status_code=200)
# def get_(, user=Depends(auth_handler.auth_wrapper)):
#    try:
#        with SessionManager() as db:
#            resp = sv.
#        return resp
#    except Exception as err:
#        raise HTTPException(400, {"title": "error",
#                            "error_message": f"{err}"})
