from backend.state import STATE, GRAPH
from backend.utils.pathfinding import dijkstra
from backend.utils.Enums import RobotStatus, OrderStatus

def assign_nearest_idle_robot(order):
    idle_robots = [r for r in STATE["robots"] if r.status == RobotStatus.IDLE]
    if not idle_robots:
        return None

    candidates = []
    for robot in idle_robots:
        dist, path = dijkstra(GRAPH, robot.node, order.source)
        candidates.append((dist, robot.name, robot, path))

    # Sort by distance, then robot name
    candidates.sort()
    _, _, selected_robot, path_to_source = candidates[0]

    # Plan full route: robot → source → target
    _, path_to_target = dijkstra(GRAPH, order.source, order.target)
    full_path = path_to_source + path_to_target[1:]

    # Update state
    selected_robot.status = RobotStatus.EXECUTING
    order.status = OrderStatus.IN_PROGRESS
    STATE["routes"] = STATE.get("routes", []) + [{
        "robot": selected_robot.name,
        "path": full_path,
        "order": order.name,
    }]
    return selected_robot.name
