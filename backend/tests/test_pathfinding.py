from backend.utils.dijkstra import dijkstra
from backend.model.Graph import GraphNode, GraphEdge, Graph
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db

def test_dijkstra_returns_valid_path():
    db: Session = next(get_db())

    # Ensure graph is seeded
    nodes = db.query(GraphNode).all()
    edges = db.query(GraphEdge).all()

    assert len(nodes) > 0, "Graph nodes not seeded"
    assert len(edges) > 0, "Graph edges not seeded"

    # Build graph schema
    graph = Graph(
        nodes=[n.to_schema() for n in nodes],
        edges=[e.to_schema() for e in edges]
    )

    # Run Dijkstra
    cost, path = dijkstra(graph, "A", "D")

    # Validate result
    assert cost > 0, f"Expected positive cost, got {cost}"
    assert path[0] == "A", f"Path should start at A, got {path[0]}"
    assert path[-1] == "D", f"Path should end at D, got {path[-1]}"
    assert all(isinstance(n, str) for n in path), f"Path contains non-string nodes: {path}"
    assert len(path) >= 2, f"Path too short: {path}"
