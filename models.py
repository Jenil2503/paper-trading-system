from sqlalchemy import(Column, Integer, String, Float,DateTime, ForeignKey, UniqueConstraint, func)

from sqlalchemy.orm import declarative_base

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'
    
    id = Column(Integer, primary_key = True)
    email = Column(String, unique = True, nullable = False)
    hashed_password = Column(String, nullable = False)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    
    
    
class Account(Base):
    __tablename__ = 'accounts'
    
    id = Column(Integer,primary_key = True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable = False, unique = True)
    cash_balance = Column(Float, nullable = False, default = 100000.0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    
class Position(Base):
    __tablename__ = "positions"
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    symbol = Column(String, nullable = False)
    quantity = Column(Integer, nullable = False, default = 0)
    avg_entry_price = Column(Float, nullable = False, default = 0.0)
    created_at = Column(DateTime(timezone = True), server_default = func.now())
    
    __table_args__ = (UniqueConstraint("user_id", "symbol", name = "uq_user_symbol"),)
    
    
class Trade(Base):
    __tablename__ = "trades"
    
    id = Column(Integer, primary_key = True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable = False)
    symbol = Column(String, nullable = False)
    side = Column(String, nullable = False)
    quantity = Column(Integer, nullable = False)
    price = Column(Float, nullable = False)
    executed_at = Column(DateTime(timezone = True), server_default = func.now())