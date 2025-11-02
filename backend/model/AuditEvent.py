from pydantic import BaseModel, Field
from typing import Literal
from datetime import datetime

class AuditEvent(BaseModel):
    timestamp: datetime = Field(..., example="2025-11-02T16:03:00Z")
    type: Literal["ORDER_CREATED", "ORDER_ASSIGNED", "ROBOT_MOVED", "ORDER_COMPLETED"]
    details: dict = Field(..., example={"order": "O-1234", "robot": "R1", "node": "B"})
