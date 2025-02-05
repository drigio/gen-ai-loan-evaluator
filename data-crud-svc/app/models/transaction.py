from pydantic import BaseModel
from typing import Optional
from datetime import date

class Transaction(BaseModel):
    id: Optional[str] = None
    date: date = None
    description: str = None
    transaction_type: str = None
    amount: float = None
    balance: float = None 
    currency: str = None