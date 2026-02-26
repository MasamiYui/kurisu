import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    String,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.sql import func

from app.models.base import Base

class RiskEvent(Base):
    __tablename__ = "risk_events"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_type = Column(String(50), nullable=False)  # margin_call/liquidation_warning/drawdown_limit/api_error
    severity = Column(String(20), nullable=False)  # info/warning/critical
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(50), nullable=False)
    details = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    resolved_at = Column(DateTime(timezone=True))

    __table_args__ = (
        Index("idx_risk_events_created_severity", created_at, severity),
    )
