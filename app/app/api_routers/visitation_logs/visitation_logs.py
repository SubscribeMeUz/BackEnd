import logging
from fastapi import APIRouter, Depends, HTTPException, Query, Request
from typing import List
from app.middleware.auth import AuthHandler
from app.db.database import SessionManager
from app.app.services.visitation_logs import visitation_logs as sv
from app.app.schemas.visitation_logs import visitation_logs as sc


router = APIRouter(prefix='/visitations', tags=['User visitations history'])
logger = logging.getLogger(__name__)
auth_handler = AuthHandler()


@router.get('/get/{id}', response_model=sc.VisitationLogOut)
def get_api(id: int, request: Request, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_visitation_log(db=db, log_id=id, request=request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.get('/my-logs', response_model=List[sc.ProviderTreeOut])
def get_user_visitations(http_request: Request,
                         aboniment_id: int = Query(None),
                         provider_id: int = Query(None),
                         user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.get_user_visitations(db=db, user=user,
                                           aboniment_id=aboniment_id,
                                           provider_id=provider_id,
                                           http_request=http_request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                            "error_message": f"{err}"})


@router.post('/add', response_model=sc.AddedNewVisitationLog)
def post_api(request: sc.VisitationLogAddRequest,
             http_request: Request,
             user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = sv.add_visitation_log(db=db, request=request, http_request=http_request)
        return resp
    except Exception as err:
        raise HTTPException(400, {"title": "error",
                                  "error_message": f"{err}"})

from app.models.visitation_logs.visitation_logs import VisitationLogs
@router.delete('/delete/{id}', status_code=200)
def get_(id: int, user=Depends(auth_handler.auth_wrapper)):
    try:
        with SessionManager() as db:
            resp = db.query(VisitationLogs).filter(VisitationLogs.id == id).first()
            db.delete(resp)
            db.commit()
        return {'result': 'deleted!'}
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
