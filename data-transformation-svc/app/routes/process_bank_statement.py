from fastapi import APIRouter, HTTPException, UploadFile, File
from typing import Any

from pydantic import ValidationError
from app.models.applicant import Applicant
from app.models.transaction import Transaction
from app.services.pdf_parser import parse_pdf
from app.services.llm_processor import process_text_with_llm
from app.services.data_crud_client import DataCRUDClient
import uuid
import inspect
from datetime import datetime


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

        return {
            "message": "Bank statement processed and transactions extracted successfully",
            "applicant_id": applicant_id,
        }

    except HTTPException as http_exc:
        raise http_exc
    except Exception as e:
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


async def process_and_store_transactions(applicant_id: str, raw_text: str) -> None:
    print("Reached " + inspect.currentframe().f_code.co_name)
    transactions_csv_list = await process_text_with_llm(raw_text)

    for transaction_dict in transactions_csv_list:
        transaction_dict["date"] = datetime.strptime(
            transaction_dict["date"], "%Y-%m-%d"
        )

    # transactions_list = [
    #     transaction.json(
    #         exclude_none=True
    #     )  # Use the `json()` method to serialize with datetime handling
    #     for transaction in [
    #         Transaction(**transaction_dict)
    #         for transaction_dict in transactions_csv_list
    #     ]
    # ]
    transactions_list = [
        transaction.model_dump(
            exclude_none=True
        )  # Use model_dump instead of dict to serialize
        for transaction in [
            Transaction(**transaction_dict)  # Create a Transaction object from the dict
            for transaction_dict in transactions_csv_list
        ]
    ]
    transactions_list = [
        {key: convert_datetime_to_string(value) for key, value in transaction.items()}
        for transaction in transactions_list
    ]
    # print("Processed transactions")
    # print(transactions_list)

    try:
        response = await data_crud_client.create_transactions(
            applicant_id, transactions_list
        )
    except HTTPException as e:
        # Catch the HTTPException (422 or other HTTP status codes)
        if e.status_code == 422:
            # Log the validation error details in the console
            print(f"Validation error occurred: {e.detail}")
            print(f"Error response: {e.response.json()}")
        else:
            print(f"HTTP error occurred: {e}")

    except ValidationError as e:
        print(f"Pydantic validation error: {e.json()}")

    if not response:
        raise HTTPException(status_code=500, detail="Failed to store transactions")

def convert_datetime_to_string(obj):
    if isinstance(obj, datetime):
        return obj.isoformat()  # Convert datetime to ISO format string
    return obj