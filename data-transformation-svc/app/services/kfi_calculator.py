# ./data-transformation-svc/app/services/kfi_calculator.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import inspect
from app.models.key_financial_indicator import KeyFinancialIndicator


def calculate_kfi(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    """
    Calculates Key Financial Indicators (KFIs) from a list of transactions.

    Args:
        transactions: A list of dictionaries, where each dictionary represents a transaction.

    Returns:
        A dictionary containing the calculated KFIs, with NaN values replaced by appropriate defaults.
    """
    print("Reached " + inspect.currentframe().f_code.co_name)
    df = pd.DataFrame(transactions)

    if df.empty:
        # Return a dictionary with default values (all 0.0 for consistency)
        return KeyFinancialIndicator().model_dump(exclude_none=True)

    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    df["amount"] = pd.to_numeric(df["amount"], errors="coerce").fillna(0)
    df["balance"] = pd.to_numeric(df["balance"], errors="coerce").fillna(0)
    df["transaction_type"] = df["transaction_type"].astype(str)

    monthly_income = (
        df[df["transaction_type"] == "credit"].groupby("month")["amount"].sum()
    )
    monthly_expenses = (
        df[df["transaction_type"] == "debit"].groupby("month")["amount"].sum()
    )

    monthly_data = pd.DataFrame(
        {
            "monthly_income": monthly_income,
            "monthly_expenses": monthly_expenses,
        }
    )
    monthly_data = monthly_data.fillna(0)
    monthly_data["net_monthly_income"] = (
        monthly_data["monthly_income"] - monthly_data["monthly_expenses"]
    )

    total_credits = df[df["transaction_type"] == "credit"]["amount"].sum()
    total_debits = df[df["transaction_type"] == "debit"]["amount"].sum()
    months_in_period = df["month"].nunique()

    MI = total_credits / months_in_period if months_in_period > 0 else 0.0
    ME = total_debits / months_in_period if months_in_period > 0 else 0.0
    NMI = MI - ME

    if total_credits + total_debits > 0:
        SR = total_credits / (total_credits + total_debits)
    else:
        SR = 0.0

    average_account_balance = df["balance"].mean()

    # Liquidity Ratio: Fallback to 0.0 if expenses are 0
    LR = average_account_balance / ME if ME != 0 else 0.0

    # Coefficient of Variation: Calculate std and mean separately, then divide
    income_std = monthly_data["monthly_income"].std()
    income_mean = monthly_data["monthly_income"].mean()
    income_cv = income_std / income_mean if income_mean != 0 else 0.0

    expense_std = monthly_data["monthly_expenses"].std()
    expense_mean = monthly_data["monthly_expenses"].mean()
    expense_cv = expense_std / expense_mean if expense_mean != 0 else 0.0

    overdrafts = df[df["balance"] < 0].shape[0]

    S_IS = 1 / (1 + income_cv) if income_cv != 0 else 1.0
    S_ES = 1 / (1 + expense_cv) if expense_cv != 0 else 1.0
    S_SR = SR
    S_LR = min(LR / 2, 1) if LR >= 0 else 0.0
    S_OP = 1 - min(overdrafts / 5, 1)

    # Helper function to handle NaN values
    def replace_nan(value):
        return 0.0 if pd.isna(value) else float(value)

    return {
        "monthly_income": replace_nan(MI),
        "monthly_expenses": replace_nan(ME),
        "net_monthly_income": replace_nan(NMI),
        "income_coefficient_of_variation": replace_nan(income_cv),
        "expense_coefficient_of_variation": replace_nan(expense_cv),
        "savings_rate": replace_nan(SR),
        "average_account_balance": replace_nan(average_account_balance),
        "liquidity_ratio": replace_nan(LR),
        "number_of_overdrafts": int(overdrafts),  # Overdrafts are always integers
        "income_stability_score": replace_nan(S_IS),
        "expense_stability_score": replace_nan(S_ES),
        "savings_rate_score": replace_nan(S_SR),
        "liquidity_ratio_score": replace_nan(S_LR),
        "overdraft_penalty_score": replace_nan(S_OP),
    }