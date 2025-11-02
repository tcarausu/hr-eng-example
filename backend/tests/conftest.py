import pytest
from backend.state import STATE, GRAPH, SEED_ORDERS, SEED_ROBOTS

@pytest.fixture(autouse=True)
def reset_state():
    STATE["orders"] = list(SEED_ORDERS)
    STATE["robots"] = list(SEED_ROBOTS)
    STATE["routes"] = []
