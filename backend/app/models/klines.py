import uuid
from datetime import datetime

from sqlalchemy import (
    BigInteger,
    Column,
    DateTime,
    Integer,
    Numeric,
    String,
    UniqueConstraint,
    Index,
)
from sqlalchemy.sql import func

from app.models.base import Base

class Kline(Base):
    __tablename__ = "klines"

    # id: BigInt 自增主键 (可选，TimescaleDB 建议尽量少用自增主键，主要依赖时间分区)
    # 既然文档说可选且不建议，我们这里先保留以防万一，或者直接用复合主键。
    # 考虑到 SQLAlchemy 通常需要一个主键，如果不设置 id，需要把复合主键设为 primary_key=True
    # 文档建议：唯一约束：(exchange, symbol, interval, open_time)
    # 我们这里使用 id 作为主键，但不是自增，或者使用复合主键。为了兼容性，保留 id 但非自增可能更好，或者直接用复合主键。
    # 既然是 timescaledb，通常不需要 id 列。
    # 这里我们遵循 SQLAlchemy 的习惯，使用复合主键。
    
    exchange = Column(String(50), primary_key=True, nullable=False)
    symbol = Column(String(50), primary_key=True, nullable=False)
    interval = Column(String(10), primary_key=True, nullable=False)
    open_time = Column(DateTime(timezone=True), primary_key=True, nullable=False)
    
    close_time = Column(DateTime(timezone=True), nullable=False)
    open = Column(Numeric(18, 8), nullable=False)
    high = Column(Numeric(18, 8), nullable=False)
    low = Column(Numeric(18, 8), nullable=False)
    close = Column(Numeric(18, 8), nullable=False)
    volume = Column(Numeric(18, 8), nullable=False)
    quote_volume = Column(Numeric(18, 8), nullable=False)
    trade_count = Column(Integer, nullable=False)
    taker_buy_base_volume = Column(Numeric(18, 8), nullable=False)
    taker_buy_quote_volume = Column(Numeric(18, 8), nullable=False)
    updated_at = Column(
        DateTime(timezone=True), 
        server_default=func.now(), 
        onupdate=func.now(), 
        nullable=False
    )

    __table_args__ = (
        # 唯一约束已由复合主键涵盖
        # 索引：(exchange, symbol, interval, open_time DESC) - 优化最新 K 线查询
        Index("idx_klines_latest", exchange, symbol, interval, open_time.desc()),
    )
