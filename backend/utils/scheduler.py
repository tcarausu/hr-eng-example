import json

from sqlalchemy.orm.session import Session

from backend.model.Graph import GraphNode, GraphEdge, Graph
from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.model.Route import Route
from backend.utils.audit import log_event
from backend.utils.dijkstra import dijkstra
from backend.utils.Enums import RobotStatus, OrderStatus


def assign_nearest_idle_robot(order: Order, db: Session) -> str | None:
    if order.status != OrderStatus.NEW:
        return None

    idle_robots = db.query(Robot).filter(Robot.status == RobotStatus.IDLE).all()
    if not idle_robots:
        return None

    graph_nodes = db.query(GraphNode).all()
    graph_edges = db.query(GraphEdge).all()
    graph = Graph(
        nodes=[n.to_schema() for n in graph_nodes],
        edges=[e.to_schema() for e in graph_edges]
    )

    candidates = []
    for robot in idle_robots:
        dist, path = dijkstra(graph, robot.node, order.source)
        candidates.append((dist, robot.name, robot, path))

    candidates.sort()
    _, _, selected_robot, path_to_source = candidates[0]

    _, path_to_target = dijkstra(graph, order.source, order.target)
    full_path = path_to_source + path_to_target[1:]

    selected_robot.status = RobotStatus.EXECUTING
    order.status = OrderStatus.IN_PROGRESS

    route = Route(robot=selected_robot.name, order=order.name, path=json.dumps(full_path))
    db.add(selected_robot)
    db.add(order)
    db.add(route)

    log_event(db, "ORDER_ASSIGNED", {"order": order.name, "robot": selected_robot.name})
    return selected_robot.name
