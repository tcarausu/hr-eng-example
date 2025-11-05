from backend.utils.scheduler import assign_nearest_idle_robot
from backend.model.Order import Order
from backend.model.Robot import Robot
from backend.model.Route import Route
from backend.utils.Enums import OrderStatus, RobotStatus
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db

def test_scheduler_assigns_robot():
    db: Session = next(get_db())

    # Get a NEW order
    order = db.query(Order).filter(Order.status == OrderStatus.NEW.value).first()
    assert order is not None

    # Run scheduler
    assigned = assign_nearest_idle_robot(order, db)
    db.commit()

    # Reload state
    updated_order = db.query(Order).filter(Order.name == order.name).first()
    assigned_robot = db.query(Robot).filter(Robot.name == assigned).first()
    route = db.query(Route).filter(Route.order == order.name).first()

    # Assertions
    assert assigned_robot is not None
    assert assigned_robot.status == RobotStatus.EXECUTING.value
    assert updated_order.status == OrderStatus.IN_PROGRESS.value
    assert route is not None
    assert route.order == order.name
