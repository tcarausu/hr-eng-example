from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from backend.model.Graph import Graph
from backend.state import GRAPH, STATE


class Route(BaseModel):
    robot: str
    path: List[str]

class RoutesResponse(BaseModel):
    routes: List[Route]

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/graph", response_model=Graph)
async def get_graph():
    return GRAPH

@router.get("/routes", response_model=RoutesResponse)
async def get_routes():
    return RoutesResponse(routes=STATE.get("routes", []))

@router.post("/tick")
async def tick() -> Dict[str, str]:
    return {"status": "ok", "note": "tick advanced (no-op stub)"}
