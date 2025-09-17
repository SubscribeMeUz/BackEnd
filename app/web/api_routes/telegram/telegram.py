from datetime import date, datetime
from fastapi import APIRouter, Query
from typing import List

from app.web.schemas.telegram.tg_schime import SendToTgChanel, CreatTgSettings
from app.web.services.telegram import tg_service
from app.models.telegram import tg_models
 
from app.web.services.statistics import statistics as sv
from app.web.schemas.statistics import statistics as sc
from app.web.schemas.statistics.statistics import UserAbonimentUseRequest, UserAbonimentUseResponse
from app.helpers.auth import auth

router = APIRouter(prefix='/tg', tags=['tg'])


@router.post('/send-message')
def send_message_tg_chanel(send_sms_request: SendToTgChanel,_=auth()):
    return tg_service.send_message_tg_chanel()

@router.post('/creat-tg-settings', status_code= 200)
def create_tg_chanel_settings(tg_settings: CreatTgSettings, user=auth()):
    return tg_service.create_tg_settings(tg_settings=tg_settings, user=user)