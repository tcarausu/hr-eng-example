import pytest
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db
from backend.routers.simulation_router import tick
from backend.utils.Enums import OrderStatus, RobotStatus
from backend.utils.scheduler import assign_nearest_idle_robot
from backend.model.Robot import Robot
from backend.model.Order import Order
from backend.model.Route import Route

@pytest.mark.asyncio
async def test_tick_completes_order_after_full_route():
    db: Session = next(get_db())

    # Cleanup
    db.query(Route).delete()
    db.query(Order).delete()
    db.query(Robot).delete()
    db.commit()

    # Create robot and order
    robot = Robot(name="R-1", node="A", status=RobotStatus.IDLE.value)
    order = Order(name="O-1", source="A", target="D", status=OrderStatus.NEW.value)
    db.add_all([robot, order])
    db.commit()

    # Assign robot
    assign_nearest_idle_robot(order, db)
    db.commit()

    # Fetch route
    route = db.query(Route).filter(Route.order == order.name).first()
    assert route is not None
    path = route.path
    path_length = len(eval(path))  # stored as JSON string

    # Run ticks
    for _ in range(path_length + 1):
        await tick(db)
        db.commit()

        updated_order = db.query(Order).filter(Order.name == order.name).first()
        updated_robot = db.query(Robot).filter(Robot.name == robot.name).first()
        updated_route = db.query(Route).filter(Route.order == order.name).first()

        if updated_order.status == OrderStatus.DONE.value:
            break

    # Final assertions
    assert updated_order.status == OrderStatus.DONE.value
    assert updated_robot.status == RobotStatus.IDLE.value
    assert updated_robot.node == updated_order.target
