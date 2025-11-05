from sqlalchemy import Column, BigInteger, String, ForeignKey
from backend.db.session import Base
from pydantic import BaseModel
from typing import List
import json

class Route(Base):
    __tablename__ = "routes"
    __table_args__ = {"schema": "openmind_ext"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    robot = Column(String, ForeignKey("openmind_ext.robots.name"), nullable=False)
    order = Column(String, ForeignKey("openmind_ext.orders.name"), nullable=False)
    path = Column(String, nullable=False)  # stored as JSON string

    def get_path_list(self) -> List[str]:
        return json.loads(self.path)

    def set_path_list(self, path_list: List[str]):
        self.path = json.dumps(path_list)

    class Schema(BaseModel):
        id: int
        robot: str
        order: str
        path: List[str]

        model_config = {
            "from_attributes": True
        }

    def to_schema(self) -> "Route.Schema":
        return Route.Schema(
            id=self.id,
            robot=self.robot,
            order=self.order,
            path=self.get_path_list()
        )


class RoutesResponse(BaseModel):
    routes: List[Route.Schema]
