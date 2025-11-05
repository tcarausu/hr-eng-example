import json
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend.db.db_singleton import get_db
from backend.db.reset import reset_state
from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.model.Route import RoutesResponse, Route
from backend.model.TickResponse import TickResponse
from backend.utils.Enums import RobotStatus, OrderStatus
from backend.utils.audit import log_event
from backend.utils.scheduler import assign_nearest_idle_robot
from backend.model.Graph import GraphNode, GraphEdge, Graph

router = APIRouter(prefix="/simulation", tags=["simulation"])


@router.get("/graph", response_model=Graph)
def get_graph(db: Session = Depends(get_db)):
    nodes = db.query(GraphNode).all()
    edges = db.query(GraphEdge).all()
    return Graph(
        nodes=[n.to_schema() for n in nodes],
        edges=[e.to_schema() for e in edges]
    )

@router.get("/routes", response_model=RoutesResponse)
def get_routes(db: Session = Depends(get_db)):
    routes = db.query(Route).all()
    return RoutesResponse(routes=[r.to_schema() for r in routes])


@router.post("/tick", response_model=TickResponse, tags=["simulation"], summary="Advance simulation by one tick",
             description="Moves all executing robots one step along their route. Completes orders when destination is reached. "
                         "Also triggers batch scheduling for NEW orders.")
@router.post("/tick", response_model=TickResponse)
async def tick(db: Session = Depends(get_db)) -> TickResponse:
    # Fetch all NEW orders
    new_orders = db.query(Order).filter(Order.status == OrderStatus.NEW).all()

    completed = []

    for order in new_orders:
        assigned_robot_name = assign_nearest_idle_robot(order, db)
        if assigned_robot_name:
            db.add(order)  # status updated inside assign_nearest_idle_robot

    # Fetch all routes
    routes = db.query(Route).all()

    for route in routes:
        robot = db.query(Robot).filter(Robot.name == route.robot).first()
        order = db.query(Order).filter(Order.name == route.order).first()
        path = json.loads(route.path)

        if not robot or not order or not path:
            continue

        # Move one step
        robot.node = path.pop(0)
        log_event(db, "ROBOT_MOVED", {"robot": robot.name, "node": robot.node})
        # If reached final node
        if not path:
            robot.status = RobotStatus.IDLE
            order.status = OrderStatus.DONE
            log_event(db, "ORDER_COMPLETED", {"order": order.name, "robot": robot.name})
            completed.append(route)
        else:
            route.path = json.dumps(path)

        db.add(robot)
        db.add(order)
        db.add(route)

    # Remove completed routes
    for route in completed:
        db.delete(route)

    db.commit()
    return TickResponse(status="ok", completed=[r.order for r in completed])



@router.post("/reset", summary="Reset simulation state", description="Clears all tables and seeds graph, robots, and orders.")
def reset(db: Session = Depends(get_db)):
    reset_state(db)
    return {"status": "reset complete"}