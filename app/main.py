from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime
from . import models, schemas, database
from .database import engine, get_db
from .celery_app import calculate_monthly_summary, send_transaction_notification
from .services.market_data import MarketDataService

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Finance Manager API")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = models.User(
        username=user.username,
        email=user.email,
        hashed_password=user.password  # In a real app, hash the password!
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

@app.get("/users/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.post("/users/{user_id}/transactions/", response_model=schemas.Transaction)
async def create_transaction(
    user_id: int,
    transaction: schemas.TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Session = Depends(get_db)
):
    db_transaction = models.Transaction(**transaction.dict(), user_id=user_id)
    db.add(db_transaction)
    db.commit()
    db.refresh(db_transaction)
    
    # Schedule notification task
    send_transaction_notification.delay(user_id, db_transaction.id)
    
    # Schedule monthly summary calculation
    now = datetime.now()
    calculate_monthly_summary.delay(user_id, now.month, now.year)
    
    return db_transaction

@app.get("/users/{user_id}/transactions/", response_model=List[schemas.Transaction])
def read_transactions(user_id: int, db: Session = Depends(get_db)):
    transactions = db.query(models.Transaction).filter(models.Transaction.user_id == user_id).all()
    return transactions

@app.get("/transactions/{transaction_id}", response_model=schemas.Transaction)
def read_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    return transaction

@app.put("/transactions/{transaction_id}", response_model=schemas.Transaction)
def update_transaction(
    transaction_id: int,
    transaction: schemas.TransactionCreate,
    db: Session = Depends(get_db)
):
    db_transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if db_transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    for key, value in transaction.dict().items():
        setattr(db_transaction, key, value)
    
    db.commit()
    db.refresh(db_transaction)
    return db_transaction

@app.delete("/transactions/{transaction_id}")
def delete_transaction(transaction_id: int, db: Session = Depends(get_db)):
    transaction = db.query(models.Transaction).filter(models.Transaction.id == transaction_id).first()
    if transaction is None:
        raise HTTPException(status_code=404, detail="Transaction not found")
    
    db.delete(transaction)
    db.commit()
    return {"message": "Transaction deleted successfully"}

@app.get("/market-data/latest/{symbol}")
def get_latest_market_data(symbol: str, db: Session = Depends(get_db)):
    market_service = MarketDataService(db)
    data = market_service.get_latest_data(symbol)
    if data is None:
        raise HTTPException(status_code=404, detail="Market data not found for symbol")
    return data

@app.get("/market-data/historical/{symbol}")
def get_historical_market_data(symbol: str, days: Optional[int] = 30, db: Session = Depends(get_db)):
    market_service = MarketDataService(db)
    return market_service.get_historical_data(symbol, days)

@app.post("/market-data/fetch")
async def fetch_market_data(symbols: Optional[List[str]] = None, db: Session = Depends(get_db)):
    market_service = MarketDataService(db)
    return await market_service.fetch_market_data(symbols) 