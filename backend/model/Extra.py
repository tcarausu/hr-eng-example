from typing import List

from pydantic import BaseModel


# -----------------------------
# Optional: additional stubs to support simulation (Frontend can ignore)
# -----------------------------

class Route(BaseModel):
    robot: str
    path: List[str]  # sequence of node ids


class RoutesResponse(BaseModel):
    routes: List[Route]
