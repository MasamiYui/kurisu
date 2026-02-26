import uuid
from datetime import datetime

from sqlalchemy import (
    Boolean,
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

class Order(Base):
    __tablename__ = "orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    strategy_id = Column(UUID(as_uuid=True), ForeignKey("strategies.id"), nullable=True)
    user_id = Column(UUID(as_uuid=True), nullable=True)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)  # buy/sell
    order_type = Column(String(20), nullable=False)  # market/limit/stop_loss/take_profit
    status = Column(String(20), nullable=False, default="open")  # open/closed/canceled/failed
    time_in_force = Column(String(10), default="GTC")
    price = Column(Numeric(18, 8))
    amount = Column(Numeric(18, 8), nullable=False)
    filled = Column(Numeric(18, 8), default=0)
    average_price = Column(Numeric(18, 8))
    client_order_id = Column(String(100), unique=True, nullable=True)
    exchange_order_id = Column(String(100), nullable=True)
    error_message = Column(Text)
    raw = Column(JSONB)
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    executed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now()
    )

    strategy = relationship("Strategy", back_populates="orders")
    trades = relationship("Trade", back_populates="order")

    __table_args__ = (
        Index("idx_orders_exchange_symbol", exchange, symbol),
        Index("idx_orders_exchange_order_id", exchange_order_id),
        Index("idx_orders_strategy_created", strategy_id, created_at),
        Index("idx_orders_status_created", status, created_at),
    )


class Trade(Base):
    __tablename__ = "trades"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    order_id = Column(UUID(as_uuid=True), ForeignKey("orders.id"), nullable=True)
    exchange = Column(String(50), nullable=False)
    symbol = Column(String(50), nullable=False)
    side = Column(String(10), nullable=False)  # buy/sell
    price = Column(Numeric(18, 8), nullable=False)
    amount = Column(Numeric(18, 8), nullable=False)
    fee_amount = Column(Numeric(18, 8))
    fee_currency = Column(String(20))
    is_maker = Column(Boolean, default=False)
    realized_pnl = Column(Numeric(18, 8))
    exchange_trade_id = Column(String(100))
    executed_at = Column(DateTime(timezone=True), nullable=False)
    raw = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="trades")

    __table_args__ = (
        Index("idx_trades_exchange_symbol_executed", exchange, symbol, executed_at.desc()),
        Index("idx_trades_exchange_trade_id", exchange_trade_id),
    )
