import uuid
from datetime import datetime

from sqlalchemy import (
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Index,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import func

from app.models.base import Base

class Position(Base):
    __tablename__ = "positions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)  # long/short
    size = Column(Numeric(18, 8), nullable=False)
    entry_price = Column(Numeric(18, 8), nullable=False)
    mark_price = Column(Numeric(18, 8))
    liquidation_price = Column(Numeric(18, 8))
    margin = Column(Numeric(18, 8))
    margin_mode = Column(String(20), default="isolated")  # isolated/cross
    leverage = Column(Numeric(18, 8), default=1)
    unrealized_pnl = Column(Numeric(18, 8))
    realized_pnl = Column(Numeric(18, 8))
    stop_loss = Column(Numeric(18, 8))
    take_profit = Column(Numeric(18, 8))
    last_synced_at = Column(DateTime(timezone=True), server_default=func.now())
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    __table_args__ = (
        UniqueConstraint("exchange", "symbol", "side", name="uq_positions_exchange_symbol_side"),
        Index("idx_positions_exchange_updated", exchange, updated_at),
    )
