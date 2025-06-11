from celery import Celery
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from .database import SessionLocal
from .services.market_data import MarketDataService

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

# Configure Celery
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    beat_schedule={
        'fetch-market-data-daily': {
            'task': 'app.celery_app.fetch_daily_market_data',
            'schedule': timedelta(days=1),
            'options': {'queue': 'market_data'}
        },
    }
)

@celery_app.task
def calculate_monthly_summary(user_id: int, month: int, year: int):
    """
    Example task that calculates monthly transaction summary
    """
    # This is a placeholder task - in a real app, you would query the database
    # and perform actual calculations
    return {
        'user_id': user_id,
        'month': month,
        'year': year,
        'calculated_at': datetime.utcnow().isoformat(),
        'status': 'completed'
    }

@celery_app.task
def send_transaction_notification(user_id: int, transaction_id: int):
    """
    Example task that would send a notification about a new transaction
    """
    # This is a placeholder task - in a real app, you would integrate
    # with an email service or push notification system
    return {
        'user_id': user_id,
        'transaction_id': transaction_id,
        'notification_sent_at': datetime.utcnow().isoformat(),
        'status': 'sent'
    }

@celery_app.task
def fetch_daily_market_data():
    """
    Task to fetch daily market data for configured symbols
    """
    try:
        # Create database session
        db: Session = SessionLocal()
        
        # Initialize market data service
        market_service = MarketDataService(db)
        
        # Fetch market data
        results = market_service.fetch_market_data()
        
        return {
            'status': 'success',
            'fetched_at': datetime.utcnow().isoformat(),
            'symbols_processed': len(results),
            'data': results
        }
    except Exception as e:
        return {
            'status': 'error',
            'error': str(e),
            'fetched_at': datetime.utcnow().isoformat()
        }
    finally:
        db.close() 