from typing import Dict, Any
import openai
from .base import BaseAssistant

class OpenAIAssistant(BaseAssistant):
    """OpenAI-based assistant implementation"""
    
    def __init__(self, api_key: str):
        super().__init__(api_key)
        openai.api_key = api_key
    
    async def generate_response(self, prompt: str, **kwargs) -> str:
        try:
            response = await openai.ChatCompletion.acreate(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}],
                **kwargs
            )
            return response.choices[0].message.content
        except Exception as e:
            return f"Error generating response: {str(e)}"
    
    async def analyze_transaction(self, transaction_data: Dict[str, Any]) -> Dict[str, Any]:
        prompt = f"""
        Please analyze this financial transaction:
        Amount: ${transaction_data.get('amount')}
        Category: {transaction_data.get('category')}
        Description: {transaction_data.get('description')}
        Date: {transaction_data.get('date')}
        
        Provide insights about:
        1. Spending category analysis
        2. Potential savings opportunities
        3. Budget impact
        """
        
        response = await self.generate_response(prompt)
        
        return {
            "transaction_id": transaction_data.get("id"),
            "analysis": response,
            "category": transaction_data.get("category"),
            "amount": transaction_data.get("amount")
        }
    
    async def generate_financial_advice(self, user_data: Dict[str, Any]) -> str:
        prompt = f"""
        Based on this user's financial data:
        Monthly Income: ${user_data.get('monthly_income')}
        Total Expenses: ${user_data.get('total_expenses')}
        Savings: ${user_data.get('savings')}
        Top Spending Categories: {', '.join(user_data.get('top_categories', []))}
        
        Please provide personalized financial advice focusing on:
        1. Budgeting recommendations
        2. Savings opportunities
        3. Investment suggestions
        4. Expense optimization
        """
        
        return await self.generate_response(prompt) 