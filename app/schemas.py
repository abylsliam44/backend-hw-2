from pydantic import BaseModel
from datetime import datetime, date
from typing import Optional, List

class TransactionBase(BaseModel):
    amount: float
    description: str
    category: str

class TransactionCreate(TransactionBase):
    pass

class Transaction(TransactionBase):
    id: int
    date: datetime
    user_id: int

    class Config:
        from_attributes = True

class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    transactions: List[Transaction] = []

    class Config:
        from_attributes = True

class MarketDataBase(BaseModel):
    symbol: str
    date: date
    open_price: float
    high_price: float
    low_price: float
    close_price: float
    volume: int
    source: str

class MarketDataCreate(MarketDataBase):
    pass

class MarketData(MarketDataBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 