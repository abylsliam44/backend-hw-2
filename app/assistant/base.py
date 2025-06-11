from abc import ABC, abstractmethod
from typing import Dict, Any, Optional

class BaseAssistant(ABC):
    """Base class for AI assistants"""
    
    def __init__(self, api_key: str):
        self.api_key = api_key
    
    @abstractmethod
    async def generate_response(self, prompt: str, **kwargs) -> str:
        """Generate a response from the AI assistant"""
        pass
    
    @abstractmethod
    async def analyze_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze a financial transaction and provide insights"""
        pass
    
    @abstractmethod
    async def generate_financial_advice(self, user_data: Dict[str, Any]) -> str:
        """Generate personalized financial advice based on user data"""
        pass 