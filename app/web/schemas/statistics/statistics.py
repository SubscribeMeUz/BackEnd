from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class ActiveSubscriptions(BaseModel):
    provider_id: int