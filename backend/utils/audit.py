from datetime import datetime
from sqlalchemy.orm import Session
from backend.model.AuditEvent import AuditEvent
from typing import Literal

def log_event(
    db: Session,
    event_type: Literal["ORDER_CREATED", "ORDER_ASSIGNED", "ROBOT_MOVED", "ORDER_COMPLETED"],
    details: dict
):
    event = AuditEvent(
        timestamp=datetime.utcnow(),
        type=event_type,
        details=details
    )
    db.add(event)
    db.commit()
