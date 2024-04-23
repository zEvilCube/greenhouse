from fastapi import APIRouter

router = APIRouter(prefix="/greenhouse")


# User Endpoints

@router.get("/")
async def get_status(api_key: str):
    return {}
