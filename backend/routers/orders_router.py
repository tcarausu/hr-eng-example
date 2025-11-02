from fastapi import APIRouter, HTTPException
from backend.model.Order import Order
from backend.model.API_Schema import AddOrderRequest, OrdersResponse
from backend.state import STATE, graph_nodes_set
from backend.utils.Enums import OrderStatus
from backend.utils.audit import log_event

router = APIRouter(prefix="/orders", tags=["orders"])



@router.post("/", response_model=Order, tags=["orders"], summary="Add a new order",
             description="Creates a new order and triggers scheduling if an IDLE robot is available.")
async def add_order(req: AddOrderRequest):
    nodes = graph_nodes_set()
    if req.source not in nodes or req.target not in nodes:
        raise HTTPException(status_code=400, detail="source/target must be valid graph nodes")

    if any(o.name == req.name for o in STATE["orders"]):
        raise HTTPException(status_code=409, detail="Order with this name already exists")

    order = Order(name=req.name, source=req.source, target=req.target, status=OrderStatus.NEW)
    STATE["orders"].append(order)
    log_event("ORDER_CREATED", {"order": order.name})
    return order

@router.get("/", response_model=OrdersResponse)
async def get_orders():
    return OrdersResponse(orders=STATE["orders"])
