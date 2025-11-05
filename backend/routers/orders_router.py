from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session
from backend.db.db_singleton import get_db
from backend.model.Order import Order
from backend.model.Graph import GraphNode
from backend.utils.Enums import OrderStatus
from backend.utils.audit import log_event

router = APIRouter(prefix="/orders", tags=["orders"])

@router.post("", response_model=Order.Schema)
async def add_order(req: Request, db: Session = Depends(get_db)):
    body = await req.json()

    # Validate required fields
    required_fields = {"name", "source", "target"}
    missing = required_fields - body.keys()
    if missing:
        raise HTTPException(status_code=422, detail=f"Missing fields: {', '.join(missing)}")

    # Validate graph node existence
    valid_nodes = {n.id for n in db.query(GraphNode).all()}
    if body["source"] not in valid_nodes or body["target"] not in valid_nodes:
        raise HTTPException(status_code=400, detail="source/target must be valid graph nodes")

    # Check for duplicate order name
    #todo made IDEMPOTENT
    existing = db.query(Order).filter(Order.name == body["name"]).first()
    if existing:
        existing.source = body["source"]
        existing.target = body["target"]
        existing.status = OrderStatus.NEW.value
        db.add(existing)
        db.commit()
        log_event(db, "ORDER_UPDATED", {"order": existing.name})
        return existing.to_schema()

    # Create and persist order
    order = Order(
        name=body["name"],
        source=body["source"],
        target=body["target"],
        status=OrderStatus.NEW.value
    )
    db.add(order)
    db.commit()
    log_event(db, "ORDER_CREATED", {"order": order.name})
    return order.to_schema()


@router.get("", response_model=list[Order.Schema])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [o.to_schema() for o in orders]
