from pydantic import BaseModel, Field
from backend.utils.Enums import RobotStatus, OrderStatus

class Edge(BaseModel):
    from_: str = Field(alias="from")
    to: str
    weight: float = 1.0

    class Config:
        validate_by_name = True
        json_encoders = {RobotStatus: lambda s: s.value, OrderStatus: lambda s: s.value}
