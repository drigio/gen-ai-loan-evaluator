from pydantic import BaseModel, Field
from typing import Optional, List
from .transaction import Transaction
from .key_financial_indicator import KeyFinancialIndicator

class Applicant(BaseModel):
    id: Optional[str] = None
    name: Optional[str] = None
    bank_statement_pdf_path: Optional[str] = None
    raw_bank_statement_txt: Optional[str] = None
    transactions: Optional[List[Transaction]] = None
    key_financial_indicators: Optional[KeyFinancialIndicator] = None