from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
from app.app.services.tools import tools as sv


router = APIRouter(prefix='/app/tools', tags=['App Tools'])


@router.get('/get-all', status_code=200)
def get_all_tools():
    return sv.get_all_tools()


@router.get('/icon/{tool_id}', response_class=FileResponse)
def get_tool_icon(tool_id: int):
    tool = sv.get_tool_by_id(tool_id)
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    return FileResponse(f"app/static/{tool['icon']}")
