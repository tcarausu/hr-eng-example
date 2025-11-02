from enum import Enum

class RobotStatus(str, Enum):
    """Status of a robot in the system."""
    IDLE = "IDLE"
    EXECUTING = "EXECUTING"

class OrderStatus(str, Enum):
    NEW = "NEW"
    IN_PROGRESS = "IN_PROGRESS"
    DONE = "DONE"
    FAILED = "FAILED"