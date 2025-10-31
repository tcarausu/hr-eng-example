from typing import List
from pydantic import BaseModel
from backend.model.Edge import Edge

class Graph(BaseModel):
    nodes: List[str]
    edges: List[Edge]