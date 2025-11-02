from fastapi import APIRouter

from backend.model.API_Schema import RobotsResponse
from backend.state import STATE

router = APIRouter(prefix="/robots", tags=["robots"])

@router.get("/", response_model=RobotsResponse)
async def get_robots():
    return RobotsResponse(robots=STATE["robots"])
