from fastapi import APIRouter
from pydantic import BaseModel
from typing import List, Dict

from backend.model.Graph import Graph
from backend.state import GRAPH, STATE
from backend.utils.Enums import RobotStatus, OrderStatus


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
    routes = list(STATE.get("routes", []))  # clone to avoid mutation during iteration
    completed = []

    for route in routes:
        robot = next((r for r in STATE["robots"] if r.name == route["robot"]), None)
        order = next((o for o in STATE["orders"] if o.name == route["order"]), None)
        path = route.get("path", [])

        if not robot or not order or not path:
            continue

        # Move one step
        robot.node = path.pop(0)

        # If reached final node
        if not path:
            robot.status = RobotStatus.IDLE
            order.status = OrderStatus.DONE
            completed.append(route)

    # Remove completed routes
    STATE["routes"] = [r for r in STATE.get("routes", []) if r not in completed]
    return {"status": "ok", "completed": [r["order"] for r in completed]}

