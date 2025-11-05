from typing import List
from pydantic import BaseModel

class TickResponse(BaseModel):
    status: str
    completed: List[str]