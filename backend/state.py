from typing import List, Dict

from backend.model import AuditEvent
from backend.model.Edge import Edge
from backend.model.Graph import Graph
from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.utils.Enums import RobotStatus, OrderStatus

# -----------------------------
# In-memory State (Replace with DB for prod)
# -----------------------------

STATE: Dict[str, List] = {
    "orders": [],
    "robots": [],
    "routes": [],
}

GRAPH: Graph = Graph(
    nodes=["A", "B", "C", "D", "E", "F"],
    edges=[
        Edge(**{"from": "A", "to": "B", "weight": 1}),
        Edge(**{"from": "B", "to": "C", "weight": 2}),
        Edge(**{"from": "C", "to": "D", "weight": 2}),
        Edge(**{"from": "B", "to": "E", "weight": 3}),
        Edge(**{"from": "E", "to": "F", "weight": 1}),
        Edge(**{"from": "D", "to": "F", "weight": 2}),
        # Treat edges as undirected for simplicity; callers may add both directions explicitly if desired
    ],
)

SEED_ROBOTS = [
    Robot(name="R1", status=RobotStatus.IDLE, node="A"),
    Robot(name="R2", status=RobotStatus.EXECUTING, node="C"),
    Robot(name="R3", status=RobotStatus.IDLE, node="E"),
]

SEED_ORDERS = [
    Order(name="O-1001", source="B", target="D", status=OrderStatus.NEW),
]


# -----------------------------
# Helpers
# -----------------------------

def graph_nodes_set() -> set:
    return set(GRAPH.nodes)


EVENTS: List[AuditEvent] = []
