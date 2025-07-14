import logging
from fastapi import APIRouter, Query
from app.app.services.visitation_logs import visitation_logs as sv
from app.app.schemas.visitation_logs import visitation_logs as sc
from app.helpers.auth import auth


router = APIRouter(prefix='/visitations', tags=['User visitations history'],
                   dependencies=[auth()])
logger = logging.getLogger(__name__)


@router.get('/get/{id}', response_model=sc.VisitationLogOut)
def get_api(id: int):
    return sv.get_user_visitation_log(log_id=id)


@router.get('/my-logs', response_model=sc.ListProviderTreeOut)
def get_user_visitations(aboniment_id: int = Query(None),
                         provider_id: int = Query(None),
                         user=auth()):
    return sv.get_user_visitations(user=user,
                                   aboniment_id=aboniment_id,
                                   provider_id=provider_id)


@router.post('/add', response_model=sc.AddedNewVisitationLog)
def post_api(request: sc.VisitationLogAddRequest, user=auth()):
    return sv.add_visitation_log(request=request, user=user)


@router.delete('/delete/{id}', status_code=200)
def delete_log(log_id: int):
    return sv.delete_log(log_id=log_id)
