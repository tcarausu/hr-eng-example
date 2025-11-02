from typing import List
from pydantic import BaseModel, Field
from backend.model.Order import Order
from backend.model.Robot import Robot

class AddOrderRequest(BaseModel):
    name: str
    source: str
    target: str

    class Config:
        schema_extra = {
            "example": {
                "name": "O-1234",
                "source": "A",
                "target": "D"
            }
        }

class OrdersResponse(BaseModel):
    orders: List[Order]

    class Config:
        schema_extra = {
            "example": {
                "orders": [
                    {
                        "name": "O-1234",
                        "source": "A",
                        "target": "D",
                        "status": "IN_PROGRESS"
                    }
                ]
            }
        }

class RobotsResponse(BaseModel):
    robots: List[Robot]

    class Config:
        schema_extra = {
            "example": {
                "robots": [
                    {
                        "name": "R-1",
                        "status": "IDLE",
                        "node": "A"
                    }
                ]
            }
        }
