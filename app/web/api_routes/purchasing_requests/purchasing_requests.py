import logging
from fastapi import APIRouter, HTTPException, Depends, Form, UploadFile, File, Response, Query, Request
from typing import List
from app.db.database import SessionManager
from app.middleware.auth import AuthHandler
from app.web.schemas.purchasing_requests import purchasing_requests as sc
from app.web.services.purchasing_requests import purchasing_requests as sv
from app.app.schemas.purchasing_requests import purchasing_requests as app_sc


logger = logging.getLogger(__name__)
router = APIRouter(prefix='/web/purchasing-requests', tags=['Purchasing requests'])
auth_handler = AuthHandler(check_admin=True)


@router.get('/get-news', status_code=200, response_model=List[sc.GetRequestsResponse])
def get_api(user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_new_purchasing_requests(db=db)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/set/{request_id}', status_code=200)
def post_api(request_id: int,
             request: Request,
             status: str = Query(..., description=(
                 "Status should be one of :"
                f"``{app_sc.PurchasingRequestsStatus.ACCESSED}`` | "
                f"``{app_sc.PurchasingRequestsStatus.DENIED}``"
             )),
             user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.set_purchasing_request_status(db=db, base_request=request,
                                            request_id=request_id, status=status)
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
