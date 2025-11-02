from typing import List
from pydantic import BaseModel
from backend.model.Order import Order
from backend.model.Robot import Robot


class AddOrderRequest(BaseModel):
    name: str
    source: str
    target: str

# Optional: include computed assignment in future
class OrdersResponse(BaseModel):
    orders: List[Order]

class RobotsResponse(BaseModel):
    robots: List[Robot]
