from pydantic import BaseModel
from typing import Optional

class KeyFinancialIndicator(BaseModel):
    id: Optional[str] = None
    monthly_income: float = None
    monthly_expenses: float = None
    net_monthly_income: float = None
    income_coefficient_of_variation: float = None
    expense_coefficient_of_variation: float = None
    savings_rate: float = None
    average_account_balance: float = None
    liquidity_ratio: float = None
    number_of_overdrafts: int = None
    income_stability_score: float = None
    expense_stability_score: float = None
    savings_rate_score: float = None
    liquidity_ratio_score: float = None
    overdraft_penalty_score: float = None