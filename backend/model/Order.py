from pydantic import BaseModel
from backend.utils.Enums import OrderStatus

class Order(BaseModel):
    name: str
    source: str
    target: str
    status: OrderStatus = OrderStatus.NEW

