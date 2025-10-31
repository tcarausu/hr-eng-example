from fastapi import APIRouter

from backend.routers.orders_router import router as orders_router
from backend.routers.robots_router import router as robots_router
from backend.routers.simulation_router import router as simulation_router

router = APIRouter(tags=["core"])

# Include sub-routers with domain-specific prefixes
router.include_router(orders_router)
router.include_router(robots_router)
router.include_router(simulation_router)

# Global health check
@router.get("/health")
async def health():
    return {"ok": True}
