"""Decorators for route functions to wrap them with try/except and DB session handling."""

import types
import inspect
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


def wrap_func(func):
    if inspect.iscoroutinefunction(func):
        async def async_wrapped(*args, **kwargs):
            try:
                if 'db' in inspect.signature(func).parameters:
                    with SessionManager() as db:
                        kwargs.setdefault('db', db)
                        return await func(*args, **kwargs)
                else:
                    return await func(*args, **kwargs)
            except HTTPException as err:
                raise err
            except Exception as err:
                raise HTTPException(400, {
                    "title": "error",
                    "error_message": str(err)
                }) from err
        return async_wrapped
    else:
        def sync_wrapped(*args, **kwargs):
            try:
                if 'db' in inspect.signature(func).parameters:
                    with SessionManager() as db:
                        kwargs.setdefault('db', db)
                        return func(*args, **kwargs)
                else:
                    return func(*args, **kwargs)
            except HTTPException as err:
                raise err
            except Exception as err:
                raise HTTPException(400, {
                    "title": "error",
                    "error_message": str(err)
                }) from err
        return sync_wrapped


def wrap_modules(MODULES: list):
    for mod in MODULES:
        for attr_name in dir(mod):
            if not attr_name.startswith('_'):
                attr = getattr(mod, attr_name)

                if (
                    isinstance(attr, types.FunctionType)
                    and attr.__module__ == mod.__name__
                ):
                    setattr(mod, attr_name, wrap_func(attr))
