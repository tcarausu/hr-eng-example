from typing import List

from pydantic import BaseModel

class Route(BaseModel):
    robot: str
    order: str
    path: List[str]

class RoutesResponse(BaseModel):
    routes: List[Route]
