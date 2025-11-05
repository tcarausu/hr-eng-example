from sqlalchemy import Column, String
from backend.db.session import Base
from pydantic import BaseModel

class Robot(Base):
    __tablename__ = "robots"
    __table_args__ = {"schema": "openmind_ext"}

    name = Column(String, primary_key=True)
    status = Column(String, nullable=False)
    node = Column(String, nullable=False)

    # -----------------------------
    # Pydantic integration
    # -----------------------------
    class Schema(BaseModel):
        name: str
        status: str
        node: str

        model_config = {
            "from_attributes": True
        }

    def to_schema(self) -> "Robot.Schema":
        return Robot.Schema.model_validate(self)
