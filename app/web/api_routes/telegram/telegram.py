from datetime import date, datetime
from fastapi import APIRouter, Query
from typing import List

from app.web.schemas.telegram.tg_schime import SendToTgChanel
from app.web.services.telegram import tg_service
from app.models.telegram import tg_models
 
from app.web.services.statistics import statistics as sv
from app.web.schemas.statistics import statistics as sc
from app.web.schemas.statistics.statistics import UserAbonimentUseRequest, UserAbonimentUseResponse
from app.helpers.auth import auth

router = APIRouter(prefix='/tg', tags=['tg'])


@router.post('/send-message')
def send_message_tg_chanel(send_sms_request: SendToTgChanel):
    return