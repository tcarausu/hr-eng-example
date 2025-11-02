from backend.utils.scheduler import assign_nearest_idle_robot
from backend.state import STATE

def test_scheduler_assigns_robot():
    order = STATE["orders"][0]
    assigned = assign_nearest_idle_robot(order)
    assert assigned in [r.name for r in STATE["robots"]]
    assert order.status == "IN_PROGRESS"
    assert any(r.status == "EXECUTING" for r in STATE["robots"])
    assert any(route.order == order.name for route in STATE["routes"])
