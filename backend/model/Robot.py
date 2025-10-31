from pydantic import BaseModel
from backend.utils.Enums import RobotStatus

class Robot(BaseModel):
    name: str
    status: RobotStatus
    node: str

