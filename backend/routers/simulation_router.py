from fastapi import APIRouter
from backend.model.Graph import Graph
from backend.model.Route import RoutesResponse
from backend.model.TickResponse import TickResponse
from backend.state import GRAPH, STATE
from backend.utils.Enums import RobotStatus, OrderStatus
from backend.utils.audit import log_event
from backend.utils.scheduler import assign_nearest_idle_robot

router = APIRouter(prefix="/simulation", tags=["simulation"])

@router.get("/graph", response_model=Graph)
async def get_graph():
    return GRAPH

@router.get("/routes", response_model=RoutesResponse)
async def get_routes():
    return RoutesResponse(routes=STATE.get("routes", []))

@router.post("/tick", response_model=TickResponse, tags=["simulation"], summary="Advance simulation by one tick",
             description="Moves all executing robots one step along their route. Completes orders when destination is reached. "
                         "Also triggers batch scheduling for NEW orders.")
async def tick() -> TickResponse:
    # Assign all NEW orders to IDLE robots
    for order in STATE["orders"]:
        if order.status == OrderStatus.NEW:
            assign_nearest_idle_robot(order)

    completed = []

    for route in STATE["routes"]:
        robot = next((r for r in STATE["robots"] if r.name == route.robot), None)
        order = next((o for o in STATE["orders"] if o.name == route.order), None)
        path = route.path

        if not robot or not order or not path:
            continue

        # Move one step
        robot.node = path.pop(0)
        log_event("ROBOT_MOVED", {"robot": robot.name, "node": robot.node})

        # If reached final node
        if not path:
            robot.status = RobotStatus.IDLE
            order.status = OrderStatus.DONE
            log_event("ORDER_COMPLETED", {"order": order.name, "robot": robot.name})
            completed.append(route)

    STATE["routes"] = [r for r in STATE["routes"] if r not in completed]
    return TickResponse(status="ok", completed=[r.order for r in completed])
