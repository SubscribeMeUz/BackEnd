import logging
from fastapi import APIRouter
from app.web.services.packages import packages as sv
from app.web.schemas.packages import packages as sc
from app.helpers.auth import auth


logger = logging.getLogger(__name__)
router = APIRouter(prefix = "/web/packages", tags=['Aboniment packages'],
                   dependencies=[auth()])


@router.get('/get-all/{provider_id}', status_code=200, response_model=sc.ListAbonimentPackageOut)
def get_api(provider_id: int):
    return sv.get_all_packages(provider_id=provider_id)


@router.post('/add', status_code=200, response_model=sc.AddedOrDeletedObjectResponse)
def post_api(request: sc.AbonimentPackageAddRequest):
    return sv.add_package(request=request)


@router.put('/edit/{id}', status_code=200, response_model=sc.AbonimentPackageOut)
def post_api(id: int, request: sc.AbonimentPackageEditRequest):
    return sv.edit_package(package_id=id, request=request)


@router.delete("/delete/{id}", response_model=sc.AddedOrDeletedObjectResponse)
def delete_api(id: int):
    return sv.delete_package(package_id=id)
