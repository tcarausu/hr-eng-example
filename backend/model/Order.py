from sqlalchemy import Column, String
from backend.db.session import Base
from pydantic import BaseModel

class Order(Base):
    __tablename__ = "orders"
    __table_args__ = {"schema": "openmind_ext"}

    name = Column(String, primary_key=True)
    source = Column(String, nullable=False)
    target = Column(String, nullable=False)
    status = Column(String, nullable=False)

    # -----------------------------
    # Pydantic integration
    # -----------------------------
    class Schema(BaseModel):
        name: str
        source: str
        target: str
        status: str

        model_config = {
            "from_attributes": True  # allows creating schema from SQLAlchemy object
        }

    def to_schema(self) -> "Order.Schema":
        return Order.Schema.model_validate(self)
