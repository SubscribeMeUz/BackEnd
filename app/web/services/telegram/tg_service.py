import math
import uuid
import shutil
import logging
from fastapi import UploadFile
from typing import List
from sqlalchemy.orm import Session, joinedload, Query
import app.config.config as app_config

from app.web.schemas.telegram.tg_schime import SendToTgChanel

def send_message_tg_chanel(send_message: SendToTgChanel):

    return app_config.TG_BOT_TOKEN