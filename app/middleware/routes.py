from urllib.parse import urljoin
from fastapi import Request
from fastapi.responses import JSONResponse
from starlette.middleware.base import BaseHTTPMiddleware
import json


PATHS = [
    'images/',
    'tools/',
]


def replace_paths(data, request: Request):
    if isinstance(data, dict):
        return {k.replace('_path', '_url'): replace_paths(v, request=request) for k, v in data.items()}
    elif isinstance(data, list):
        return [replace_paths(item, request=request) for item in data]
    elif isinstance(data, str):
        for prefix in PATHS:
            if data.startswith(prefix):
                return urljoin(request.base_url.__str__(), data)
        return data
    else:
        return data


class RewriteStaticPathsMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)

        if response.headers.get("content-type", "").startswith("application/json"):
            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            try:
                raw_data = json.loads(body)
                transformed_data = replace_paths(raw_data, request=request)
                return JSONResponse(content=transformed_data, status_code=response.status_code)
            except json.JSONDecodeError:
                return response
        return response
