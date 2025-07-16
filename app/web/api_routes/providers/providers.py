import logging
from fastapi import APIRouter, UploadFile, File, Form, Query
from app.web.schemas.providers import providers as sc
from app.web.services.providers import providers as sv
from app.helpers.auth import provider_auth, admin_auth, auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/providers", tags=['Providers'])


@router.get('/get/all', status_code=200, response_model=sc.ListProviderOut)
def get_all_providers(owner=provider_auth()):
    return sv.get_all_providers(owner=owner)


@router.get('/get/all/providers', status_code=200, response_model=sc.ProvidersAllOut)
def get_providers_with_pagination(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, le=100),
    query: str = Query(None),
    owner = provider_auth()
):
    return sv.get_all_providers_with_filters(page=page,
                                             page_size=page_size,
                                             string_query=query,
                                             owner=owner)


@router.get('/get/related-by-user', status_code=200, response_model=sc.ListProviderOut)
def get_my_subcriptions(user=auth()):
    return sv.get_providers_related_by_user(user=user)


@router.get('/get/by-owner/{owner_id}', status_code=200, response_model=sc.ListProviderOut)
def get_providers_by_owner(owner_id: int, _=auth()):
    return sv.get_providers_by_owner(owner_id=owner_id)


@router.get('/get/{provider_id}', status_code=200, response_model=sc.ProviderDetailResponse)
def get_provider(provider_id: int):
    return sv.get_provider(provider_id=provider_id)


@router.post('/add', status_code=200, response_model=sc.ProviderAddedResponse)
def add_provider(name: str = Form(...),
                 location_latt: str = Form(...),
                 location_long: str = Form(...),
                 necessary_tools: str = Form(''),
                 about_description: str = Form(None),
                 logo: UploadFile = File(...),
                 owner_id: int = Form(...),
                 _=admin_auth()):
    logo_path = sv.save_file(logo)
    return sv.add_provider(name=name,
                           location_latt=location_latt,
                           location_long=location_long,
                           necessary_tools=necessary_tools,
                           about_description=about_description,
                           logo_path=logo_path,
                           owner_id=owner_id)


@router.put('/edit/{provider_id}', status_code=200)
def edit_provider(provider_id: int,
                  name: str = Form(None),
                  location_latt: str = Form(None),
                  location_long: str = Form(None),
                  about_description: str = Form(None),
                  logo: UploadFile = File(None),
                  owner_id: int = Form(None),
                  _=provider_auth()):
    logo_path = sv.save_file(logo)
    return sv.edit_provider(provider_id=provider_id,
                            name=name,
                            location_latt=location_latt,
                            location_long=location_long,
                            about_description=about_description,
                            logo_path=logo_path,
                            owner_id=owner_id)


@router.delete('/delete/{provider_id}')
def delete_provider(provider_id: int, _=admin_auth()):
    return sv.delete_provider(provider_id=provider_id)


@router.post('/add-photo/{provider_id}', status_code=200)
def post_api(provider_id: int, file: UploadFile, _=provider_auth()):
    path = sv.save_file(file=file)
    return sv.save_provider_photo(provider_id=provider_id, photo=path)    


@router.delete('/delete-photo/{photo_id}', status_code=200)
def delete_api(photo_id: int, _=provider_auth()):
    return sv.delete_photo(photo_id=photo_id)
