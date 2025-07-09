import logging
from fastapi import APIRouter, HTTPException, Depends, Query
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.services.packages import packages as sv
from app.web.schemas.packages import packages as sc


logger = logging.getLogger(__name__)
auth_handler = AuthHandler()
admin_auth_handler = AuthHandler(True)
router = APIRouter(prefix = "/web/packages", tags=['Aboniment packages'])


@router.get('/get-all/{provider_id}', status_code=200, response_model=List[sc.AbonimentPackageOut])
def get_api(provider_id: int):
    try:
        with SessionManager() as db:
            resp = sv.get_all_packages(db=db, provider_id=provider_id)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add', status_code=200, response_model=sc.AddedOrDeletedObjectRescponse)
def post_api(request: sc.AbonimentPackageAddRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_package(db=db, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.put('/edit/{id}', status_code=200, response_model=sc.AbonimentPackageOut)
def post_api(id: int, request: sc.AbonimentPackageEditRequest, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.edit_package(db=db, package_id=id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.delete("/delete/{id}", response_model=sc.AddedOrDeletedObjectRescponse)
def delete_api(id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.delete_package(db, package_id=id)
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
