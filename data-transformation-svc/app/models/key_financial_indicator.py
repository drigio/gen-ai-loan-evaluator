from pydantic import BaseModel
from typing import Optional

class KeyFinancialIndicator(BaseModel):
    id: Optional[str] = None
    monthly_income: Optional[float] = None
    monthly_expenses: Optional[float] = None
    net_monthly_income: Optional[float] = None
    income_coefficient_of_variation: Optional[float] = None
    expense_coefficient_of_variation: Optional[float] = None
    savings_rate: Optional[float] = None
    average_account_balance: Optional[float] = None
    liquidity_ratio: Optional[float] = None
    number_of_overdrafts: Optional[int] = None
    income_stability_score: Optional[float] = None
    expense_stability_score: Optional[float] = None
    savings_rate_score: Optional[float] = None
    liquidity_ratio_score: Optional[float] = None
    overdraft_penalty_score: Optional[float] = None
