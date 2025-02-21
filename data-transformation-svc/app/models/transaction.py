from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class Transaction(BaseModel):
    id: Optional[str] = None
    date: Optional[datetime] = None
    description: Optional[str] = None
    transaction_type: Optional[str] = None
    amount: Optional[float] = None
    balance: Optional[float] = None
    currency: Optional[str] = None