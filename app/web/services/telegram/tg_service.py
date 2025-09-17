import requests
import math
import uuid
import shutil
import logging
from fastapi import UploadFile
from typing import List
from sqlalchemy.orm import Session, joinedload, Query

import app.config.config as app_config
from app.models.telegram.tg_models import TgSettings

from app.models.users.users import Users

from app.web.schemas.telegram.tg_schime import SendToTgChanel,CreatTgSettings

def send_message_tg_chanel():
    bot_token = app_config.TG_BOT_TOKEN
    chat_id = "-1003048415188"
    text= "hello from bot"
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    # Payload
    payload = {
        "chat_id": chat_id,
        "text": text
    }
    response = requests.post(url=url, data= payload)
    print(response.json())
    return response.json()

def create_tg_settings(db:Session,  tg_settings: CreatTgSettings, user: Users):
    tg_settings_model = TgSettings()
    tg_settings_model.chanel_name = tg_settings.chanel_name
    tg_settings_model.is_active = True

    db.add(tg_settings_model)

    try:
        db.commit()
        #db.refresh(tg_settings_model)
        return {"result" : "Ok",
                "tg_settings": tg_settings_model.id}
    except Exception as err:
        db.rollback()
        raise err 
