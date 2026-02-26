import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
    Index,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.models.base import Base

class Strategy(Base):
    __tablename__ = "strategies"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text)
    code = Column(Text)
    parameters = Column(JSONB)
    version = Column(Integer, default=1)
    status = Column(String(20), default="draft")  # draft/active/archived
    risk_level = Column(String(20), default="medium")  # low/medium/high
    max_position_size = Column(Numeric(18, 8))
    allowed_symbols = Column(JSONB)
    created_by = Column(String(100))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    runs = relationship("StrategyRun", back_populates="strategy")
    orders = relationship("Order", back_populates="strategy")


class StrategyRun(Base):
    __tablename__ = "strategy_runs"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=False)
    started_at = Column(DateTime(timezone=True), server_default=func.now())
    ended_at = Column(DateTime(timezone=True))
    status = Column(String(20), default="running")  # running/completed/failed
    total_pnl = Column(Numeric(18, 8), default=0)
    trade_count = Column(Integer, default=0)
    error_message = Column(Text)
    context = Column(JSONB)

    strategy = relationship("Strategy", back_populates="runs")

    __table_args__ = (
        Index("idx_strategy_runs_strategy_started", strategy_id, started_at.desc()),
    )
