from fastapi import APIRouter, HTTPException, Request
from typing import List
from bson.objectid import ObjectId
from app.db import get_db
from app.models.transaction import Transaction

router = APIRouter()


@router.post(
    "/applicants/{applicant_id}/transactions/",
    response_model=Transaction,
    status_code=201,
)
async def create_transaction(applicant_id: str, transaction: Transaction):
    db = get_db()
    result = db.transactions.insert_one(transaction.model_dump(exclude_unset=True))
    transaction.id = str(result.inserted_id)
    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$push": {"transactions": transaction.model_dump()}},
    )
    return transaction


@router.post(
    "/applicants/{applicant_id}/transactions/bulk/",
    status_code=201,
)
async def create_bulk_transactions(applicant_id: str, transactions: List[Transaction], request: Request):
    """
    Bulk creates transactions for an applicant.
    """
    raw_body = await request.json()  # Parse the raw JSON body
    # print("Raw Request Body:", raw_body)

    # print(transactions)
    transaction_dicts = [
        transaction.model_dump(exclude_unset=True) for transaction in transactions
    ]

    # print("transactions_dicts STARTS HERE =============================\n\n")

    db = get_db()
    result = db.transactions.insert_many(transaction_dicts)
    inserted_ids = result.inserted_ids

    created_transactions = []
    transaction_dumps_for_applicant = []

    for i, transaction in enumerate(transactions):
        transaction.id = str(inserted_ids[i])
        created_transactions.append(transaction)
        transaction_dumps_for_applicant.append(
            transaction.model_dump()
        )  # Use model_dump here to keep consistency with single transaction endpoint

    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$push": {"transactions": {"$each": transaction_dumps_for_applicant}}},
    )
    return {"message": "Transactions have been added"}


@router.get(
    "/applicants/{applicant_id}/transactions/{transaction_id}",
    response_model=Transaction,
)
async def get_transaction(applicant_id: str, transaction_id: str):
    db = get_db()
    transaction = db.transactions.find_one(
        {"_id": ObjectId(transaction_id), "is_deleted": {"$ne": True}}
    )
    if transaction:
        transaction["id"] = str(transaction["_id"])
        return Transaction(**transaction)
    raise HTTPException(status_code=404, detail="Transaction not found")


@router.get(
    "/applicants/{applicant_id}/transactions/", response_model=List[Transaction]
)
async def get_transactions(applicant_id: str):
    db = get_db()
    applicant = db.applicants.find_one(
        {"_id": ObjectId(applicant_id), "is_deleted": {"$ne": True}}
    )
    if not applicant:
        raise HTTPException(status_code=404, detail="Applicant not found")
    transactions_data = applicant.get("transactions", [])
    transactions = [Transaction(**transaction) for transaction in transactions_data]
    return transactions


@router.put(
    "/applicants/{applicant_id}/transactions/{transaction_id}",
    response_model=Transaction,
)
async def update_transaction(
    applicant_id: str, transaction_id: str, transaction: Transaction
):
    db = get_db()
    result = db.transactions.update_one(
        {"_id": ObjectId(transaction_id)},
        {"$set": transaction.model_dump(exclude_unset=True)},
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.applicants.update_one(
        {"_id": ObjectId(applicant_id), "transactions.id": transaction_id},
        {"$set": {"transactions.$[element]": transaction.model_dump()}},
        array_filters=[
            {"element.id": transaction_id}
        ],  # More robust update using array_filters
    )
    return transaction


@router.delete(
    "/applicants/{applicant_id}/transactions/{transaction_id}", status_code=200
)
async def delete_transaction(applicant_id: str, transaction_id: str):
    db = get_db()
    result = db.transactions.update_one(
        {"_id": ObjectId(transaction_id)}, {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Transaction not found")

    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$pull": {"transactions": {"id": transaction_id}}},
    )
    return {"message": "Transaction soft deleted"}
