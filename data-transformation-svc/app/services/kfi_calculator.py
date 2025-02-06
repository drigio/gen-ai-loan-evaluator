# ./data-transformation-svc/app/services/kfi_calculator.py
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import inspect
from app.models.key_financial_indicator import KeyFinancialIndicator


def calculate_kfi(transactions: List[Dict[str, Any]]) -> Dict[str, Any]:
    print("Reached " + inspect.currentframe().f_code.co_name)
    # Convert transactions to DataFrame for easier processing
    df = pd.DataFrame(transactions)

    if df.empty:
        return KeyFinancialIndicator().model_dump(
            exclude_none=True
        )  # Return default values
    df["date"] = pd.to_datetime(df["date"])
    df["month"] = df["date"].dt.to_period("M")

    # Ensure correct types, handling None values properly
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

    MI = total_credits / months_in_period if months_in_period > 0 else 0
    ME = total_debits / months_in_period if months_in_period > 0 else 0
    NMI = MI - ME
    SR = NMI / MI if MI != 0 else np.nan
    average_account_balance = df["balance"].mean()
    LR = average_account_balance / ME if ME != 0 else np.nan

    income_cv = (
        monthly_data["monthly_income"].std() / monthly_data["monthly_income"].mean()
        if monthly_data["monthly_income"].mean() != 0
        else 0
    )
    expense_cv = (
        monthly_data["monthly_expenses"].std() / monthly_data["monthly_expenses"].mean()
        if monthly_data["monthly_expenses"].mean() != 0
        else 0
    )

    overdrafts = df[df["balance"] < 0].shape[0]

    S_IS = 1 / (1 + income_cv) if income_cv != 0 else 1
    S_ES = 1 / (1 + expense_cv) if expense_cv != 0 else 1
    S_SR = SR if not np.isnan(SR) else 0
    S_LR = min(LR / 2, 1) if not np.isnan(LR) else 0
    S_OP = 1 - min(overdrafts / 5, 1)

    return {
        "monthly_income": MI,
        "monthly_expenses": ME,
        "net_monthly_income": NMI,
        "income_coefficient_of_variation": income_cv,
        "expense_coefficient_of_variation": expense_cv,
        "savings_rate": S_SR,  # Use the Score (0-1 range)
        "average_account_balance": average_account_balance,
        "liquidity_ratio": LR,
        "number_of_overdrafts": overdrafts,
        "income_stability_score": S_IS,
        "expense_stability_score": S_ES,
        "savings_rate_score": S_SR,
        "liquidity_ratio_score": S_LR,
        "overdraft_penalty_score": S_OP,
    }
