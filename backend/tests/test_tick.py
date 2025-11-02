import pytest

from backend.routers.simulation_router import tick
from backend.state import STATE
from backend.utils.Enums import OrderStatus, RobotStatus
from backend.utils.scheduler import assign_nearest_idle_robot
from backend.model.Robot import Robot
from backend.model.Order import Order

@pytest.mark.asyncio
async def test_tick_completes_order_after_full_route():
    # Reset state
    STATE["orders"] = []
    STATE["robots"] = []
    STATE["routes"] = []

    # Create robot and order using model classes
    robot = Robot(name="R-1", node="A", status=RobotStatus.IDLE)
    order = Order(name="O-1", source="A", target="D", status=OrderStatus.NEW)

    STATE["robots"].append(robot)
    STATE["orders"].append(order)

    # Assign robot
    assign_nearest_idle_robot(order)

    # Get route
    route = next(r for r in STATE["routes"] if r.order == order.name)
    path_length = len(route.path)

    # Debug: confirm route and target
    print("Assigned route:", route.path)
    print("Expected target:", order.target)

    # Run ticks
    for i in range(path_length + 1):
        print("Before tick:", route.path)
        await tick()
        print("After tick:", route.path)
        print(f"Tick {i + 1}: robot at {robot.node}, order status = {order.status}")
        if order.status == OrderStatus.DONE:
            break

    # Final assertions
    print("Final robot node:", robot.node)
    print("Final order status:", order.status)

    assert order.status == OrderStatus.DONE
    assert robot.status == RobotStatus.IDLE
    assert robot.node == order.target
