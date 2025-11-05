import heapq
from math import inf

from backend.model.Graph import Graph


def dijkstra(graph: Graph, start: str, end: str) -> tuple[int, list[str]]:
    queue = [(0, start, [])]
    visited = set()

    while queue:
        cost, node, path = heapq.heappop(queue)
        if node in visited:
            continue
        visited.add(node)
        path = path + [node]
        if node == end:
            return cost, path

        for edge in graph.edges:
            neighbors = []
            if edge.from_node == node:
                neighbors.append(edge.to_node)
            elif edge.to_node == node:
                neighbors.append(edge.from_node)

            for neighbor in neighbors:
                if neighbor not in visited:
                    heapq.heappush(queue, (int(cost + edge.weight), neighbor, path.copy()))

    return int(inf), []