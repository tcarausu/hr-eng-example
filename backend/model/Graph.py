from sqlalchemy import Column, String, BigInteger, Float, ForeignKey
from backend.db.session import Base
from pydantic import BaseModel
from typing import List

class GraphNode(Base):
    __tablename__ = "graph_nodes"
    __table_args__ = {"schema": "openmind_ext"}
    id = Column(String, primary_key=True)

    class Schema(BaseModel):
        id: str

        model_config = {
            "from_attributes": True
        }

    def to_schema(self) -> "GraphNode.Schema":
        return GraphNode.Schema.model_validate(self)


class GraphEdge(Base):
    __tablename__ = "graph_edges"
    __table_args__ = {"schema": "openmind_ext"}
    id = Column(BigInteger, primary_key=True, autoincrement=True)
    from_node = Column(String, ForeignKey("openmind_ext.graph_nodes.id"), nullable=False)
    to_node = Column(String, ForeignKey("openmind_ext.graph_nodes.id"), nullable=False)
    weight = Column(Float, default=1.0)

    class Schema(BaseModel):
        from_node: str
        to_node: str
        weight: float

        model_config = {
            "from_attributes": True
        }

    def to_schema(self) -> "GraphEdge.Schema":
        return GraphEdge.Schema.model_validate(self)


class Graph(BaseModel):
    nodes: List[GraphNode.Schema]
    edges: List[GraphEdge.Schema]
