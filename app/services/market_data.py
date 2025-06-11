import yfinance as yf
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from ..models import MarketData

class MarketDataService:
    def __init__(self, db: Session):
        self.db = db
        self.default_symbols = [
            "AAPL",  # Apple
            "MSFT",  # Microsoft
            "GOOGL", # Google
            "AMZN",  # Amazon
            "BTC-USD",  # Bitcoin
            "ETH-USD",  # Ethereum
        ]

    async def fetch_market_data(self, symbols: List[str] = None) -> List[Dict[str, Any]]:
        """
        Fetch market data for given symbols from Yahoo Finance
        """
        if symbols is None:
            symbols = self.default_symbols

        results = []
        for symbol in symbols:
            try:
                # Get data from Yahoo Finance
                ticker = yf.Ticker(symbol)
                hist = ticker.history(period="1d")
                
                if not hist.empty:
                    data = hist.iloc[0]
                    market_data = MarketData(
                        symbol=symbol,
                        date=datetime.now().date(),
                        open_price=float(data['Open']),
                        high_price=float(data['High']),
                        low_price=float(data['Low']),
                        close_price=float(data['Close']),
                        volume=int(data['Volume']),
                        source='yahoo_finance'
                    )
                    
                    # Save to database
                    self.db.add(market_data)
                    self.db.commit()
                    self.db.refresh(market_data)
                    
                    results.append({
                        "symbol": symbol,
                        "data": {
                            "open": market_data.open_price,
                            "high": market_data.high_price,
                            "low": market_data.low_price,
                            "close": market_data.close_price,
                            "volume": market_data.volume,
                            "date": market_data.date.isoformat()
                        }
                    })
            except Exception as e:
                print(f"Error fetching data for {symbol}: {str(e)}")
                continue
        
        return results

    def get_latest_data(self, symbol: str) -> MarketData:
        """
        Get the latest market data for a symbol from the database
        """
        return self.db.query(MarketData)\
            .filter(MarketData.symbol == symbol)\
            .order_by(MarketData.date.desc())\
            .first()

    def get_historical_data(self, symbol: str, days: int = 30) -> List[MarketData]:
        """
        Get historical market data for a symbol from the database
        """
        start_date = datetime.now().date() - timedelta(days=days)
        return self.db.query(MarketData)\
            .filter(MarketData.symbol == symbol)\
            .filter(MarketData.date >= start_date)\
            .order_by(MarketData.date.asc())\
            .all() 