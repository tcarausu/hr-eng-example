from sqlalchemy import Column, BigInteger, String, TIMESTAMP, JSON, func
from backend.db.session import Base

class AuditEvent(Base):
    __tablename__ = "audit_events"
    __table_args__ = {"schema": "openmind_ext"}

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=func.now())
    type = Column(String, nullable=False)
    details = Column(JSON, nullable=False)