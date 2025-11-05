from sqlalchemy import text
from sqlalchemy.orm import Session

from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.utils.Enums import RobotStatus, OrderStatus

def reset_state(db: Session):
    # Clear all tables
    db.execute(text("DELETE FROM openmind_ext.routes"))
    db.execute(text("DELETE FROM openmind_ext.orders"))
    db.execute(text("DELETE FROM openmind_ext.robots"))
    db.execute(text("DELETE FROM openmind_ext.audit_events"))

    # Insert seed robots
    for robot in [
        Robot(name="R1", status=RobotStatus.IDLE, node="A"),
        Robot(name="R2", status=RobotStatus.EXECUTING, node="C"),
        Robot(name="R3", status=RobotStatus.IDLE, node="E"),
    ]:
        db.execute(
            text("""
                INSERT INTO openmind_ext.robots (name, status, node)
                VALUES (:name, :status, :node)
            """),
            {"name": robot.name, "status": robot.status.value, "node": robot.node}
        )

    # Insert seed orders
    for order in [
        Order(name="O-1001", source="B", target="D", status=OrderStatus.NEW),
    ]:
        db.execute(
            text("""
                INSERT INTO openmind_ext.orders (name, source, target, status)
                VALUES (:name, :source, :target, :status)
            """),
            {
                "name": order.name,
                "source": order.source,
                "target": order.target,
                "status": order.status.value,
            }
        )

    db.commit()
