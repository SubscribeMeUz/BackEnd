"""Decorators for route functions to wrap them with try/except and DB session handling."""

from functools import wraps
from fastapi.exceptions import HTTPException
from app.db.database import SessionManager


def try_except(func):
    """Decorator for synchronous route handlers to manage DB session and catch exceptions."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        try:
            with SessionManager() as db:
                kwargs['db'] = db
                return func(*args, **kwargs)
        except Exception as err:
            raise HTTPException(400, {
                "title": "error",
                "error_message": str(err)
            }) from err
    return wrapper


def try_except_async(func):
    """Decorator for async route handlers to manage DB session and catch exceptions."""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            with SessionManager() as db:
                kwargs['db'] = db
                return await func(*args, **kwargs)
        except Exception as err:
            raise HTTPException(400, {
                "title": "error",
                "error_message": str(err)
            }) from err
    return wrapper
