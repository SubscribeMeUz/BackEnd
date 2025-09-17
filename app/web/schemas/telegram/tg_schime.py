from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Literal


class SendToTgChanel(BaseModel):
    provider_id: int
    message: str

class CreatTgSettings(BaseModel):
    chanel_name: str
    is_active : bool = False 
    provider_id : int