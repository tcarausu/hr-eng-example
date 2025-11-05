import pytest
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db
from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.model.Route import Route
from backend.model.Graph import GraphNode, GraphEdge
from backend.utils.Enums import OrderStatus, RobotStatus

@pytest.fixture(autouse=True)
def seed_database():
    db: Session = next(get_db())

    try:
        # Rollback any failed transaction
        db.rollback()

        # Delete in dependency order
        db.query(Route).delete()
        db.query(Order).delete()
        db.query(Robot).delete()
        db.commit()

        # Seed robots
        db.add_all([
            Robot(name="R1", status=RobotStatus.IDLE.value, node="A"),
            Robot(name="R2", status=RobotStatus.EXECUTING.value, node="C"),
            Robot(name="R3", status=RobotStatus.IDLE.value, node="E"),
        ])

        # Seed order only if not exists
        if not db.query(Order).filter(Order.name == "O-1001").first():
            db.add(Order(name="O-1001", source="B", target="D", status=OrderStatus.NEW.value))

        # Seed graph nodes
        existing_nodes = {n.id for n in db.query(GraphNode).all()}
        for node_id in ["A", "B", "C", "D", "E", "F"]:
            if node_id not in existing_nodes:
                db.add(GraphNode(id=node_id))

        # Seed graph edges
        existing_edges = {(e.from_node, e.to_node) for e in db.query(GraphEdge).all()}
        edges_to_seed = [
            ("A", "B", 1),
            ("B", "C", 2),
            ("C", "D", 2),
            ("B", "E", 3),
            ("E", "F", 1),
            ("D", "F", 2),
        ]
        for from_node, to_node, weight in edges_to_seed:
            if (from_node, to_node) not in existing_edges:
                db.add(GraphEdge(from_node=from_node, to_node=to_node, weight=weight))

        db.commit()

    except Exception:
        db.rollback()
        raise
