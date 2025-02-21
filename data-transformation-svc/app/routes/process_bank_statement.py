# ./data-transformation-svc/app/routes/process_bank_statement.py
from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Any, Dict, List

from pydantic import ValidationError
from app.models.applicant import Applicant
from app.models.transaction import Transaction
from app.services.pdf_parser import parse_pdf
from app.services.llm_processor import process_text_with_llm
from app.services.data_crud_client import DataCRUDClient
import uuid
import inspect
from datetime import datetime
import numpy as np  # Import numpy
from app.models.key_financial_indicator import KeyFinancialIndicator
from app.services.kfi_calculator import calculate_kfi  # Import the service

router = APIRouter()
data_crud_client = DataCRUDClient()


@router.post("/process-bank-statement")
async def process_bank_statement(file: UploadFile = File(...)) -> Any:
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400, detail="Invalid file format. Please upload a PDF."
        )

    try:
        raw_text = parse_pdf(await file.read())
        applicant_id = await create_applicant()
        await update_applicant_with_raw_text(applicant_id, raw_text)
        transactions = await process_and_store_transactions(applicant_id, raw_text)
        await process_and_store_kfi(applicant_id, transactions)  # Add KFI processing

        return {
            "message": "Bank statement processed and transactions extracted successfully",
            "applicant_id": applicant_id,
        }

    except HTTPException as http_exc:
        print(http_exc)
        raise http_exc
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail=str(e))
        


async def create_applicant() -> str:
    print("Reached " + inspect.currentframe().f_code.co_name)
    applicant_name = f"Applicant-{uuid.uuid4()}"
    response = await data_crud_client.create_applicant({"name": applicant_name})
    if not response or "id" not in response:
        raise HTTPException(status_code=500, detail="Failed to create applicant")
    return response["id"]


async def update_applicant_with_raw_text(applicant_id: str, raw_text: str) -> None:
    print("Reached " + inspect.currentframe().f_code.co_name)
    applicant_data = await data_crud_client.get_applicant(applicant_id)
    if not applicant_data:
        raise HTTPException(status_code=404, detail="Applicant not found")

    applicant = Applicant(**applicant_data)
    applicant.raw_bank_statement_txt = raw_text

    response = await data_crud_client.update_applicant(
        applicant_id, applicant.dict(exclude_none=True)
    )
    if not response:
        raise HTTPException(
            status_code=500, detail="Failed to update applicant with raw text"
        )


async def process_and_store_transactions(
    applicant_id: str, raw_text: str
) -> List[Dict[str, any]]:  # Return the transaction list
    print("Reached " + inspect.currentframe().f_code.co_name)
    transactions_csv_list = await process_text_with_llm(raw_text)

    for transaction_dict in transactions_csv_list:
        transaction_dict["date"] = datetime.strptime(
            transaction_dict["date"], "%Y-%m-%d"
        )

    transactions_list = [
        transaction.model_dump(exclude_none=True)
        for transaction in [
            Transaction(**transaction_dict)
            for transaction_dict in transactions_csv_list
        ]
    ]
    transactions_list = [
        {key: convert_datetime_to_string(value) for key, value in transaction.items()}
        for transaction in transactions_list
    ]

    try:
        response = await data_crud_client.create_transactions(
            applicant_id, transactions_list
        )
        if not response:
            raise HTTPException(status_code=500, detail="Failed to store transactions")
        return transactions_list  # Return processed transactions

    except HTTPException as e:
        if e.status_code == 422:
            print(f"Validation error occurred: {e.detail}")
            print(f"Error response: {e.response.json()}")
        else:
            print(f"HTTP error occurred: {e}")
        raise  # Re-raise the exception to be caught in the main handler

    except ValidationError as e:
        print(f"Pydantic validation error: {e.json()}")
        raise HTTPException(
            status_code=500, detail="Failed to validate transaction data"
        )  # Convert ValidationError to HTTPException


def convert_datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO format string
    return obj


async def process_and_store_kfi(applicant_id: str, transactions: List[Dict[str, any]]):
    print("Reached " + inspect.currentframe().f_code.co_name)
    kfi_data = calculate_kfi(transactions)  # Use the imported function
    print(kfi_data)
    kfi_model = KeyFinancialIndicator(**kfi_data)

    try:
        response = await data_crud_client.create_kfi(
            applicant_id, kfi_model.model_dump(exclude_none=True)
        )
    except HTTPException as e:
        if e.status_code == 422:
            print(f"Validation error occurred: {e.detail}")
        else:
            print(f"HTTP error occurred: {e}")
        raise
    except ValidationError as e:
        print(
            f"Pydantic validation error: {e}"
        )  # Correct way to print validation errors.
        raise
    if not response:
        raise HTTPException(status_code=500, detail="Failed to store KFI data")
