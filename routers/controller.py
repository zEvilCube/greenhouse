from fastapi import APIRouter

from models.controller import ControllerStatus

router = APIRouter(prefix="/controller")


# Device Endpoints

@router.post("/status")
async def post_status(api_key: str, status: ControllerStatus):
    return {}
