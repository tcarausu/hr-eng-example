from backend.utils.dijkstra import dijkstra
from backend.state import GRAPH

def test_dijkstra_returns_valid_path():
    cost, path = dijkstra(GRAPH, "A", "D")
    assert cost > 0
    assert path[0] == "A"
    assert path[-1] == "D"
    assert all(isinstance(n, str) for n in path)
