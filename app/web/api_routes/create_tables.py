from fastapi import APIRouter
import logging
from app.middleware.auth import AuthHandler
from app.db.create_db import create_table


auth_handler = AuthHandler()

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix = "", tags=["Create Tables"]
)


#Создание таблиц для суперпользователя
@router.get('/create_tables', status_code=200)
def create_tables():
    logger.info("requested method create_tables")
    resp = create_table()
    logger.info(f"Tables has been succesfully created! Base: {resp}")
    return {"result": "ok", "message": resp}
