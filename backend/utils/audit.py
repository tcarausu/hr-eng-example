from datetime import datetime
from backend.model.AuditEvent import AuditEvent
from backend.state import EVENTS

from typing import Literal

def log_event(
    event_type: Literal["ORDER_CREATED", "ORDER_ASSIGNED", "ROBOT_MOVED", "ORDER_COMPLETED"],
    details: dict
):
    EVENTS.append(AuditEvent(
        timestamp=datetime.utcnow(),
        type=event_type,
        details=details
    ))
