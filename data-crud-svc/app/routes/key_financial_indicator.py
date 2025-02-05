from fastapi import APIRouter, HTTPException
from bson.objectid import ObjectId
from app.db import get_db
from app.models.key_financial_indicator import KeyFinancialIndicator

router = APIRouter()

@router.post("/applicants/{applicant_id}/kfis/", response_model=KeyFinancialIndicator, status_code=201)
async def create_kfi(applicant_id: str, kfi: KeyFinancialIndicator):
    db = get_db()
    result = db.key_financial_indicators.insert_one(kfi.model_dump(exclude_unset=True))
    kfi.id = str(result.inserted_id)
    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$set": {"key_financial_indicators": kfi.model_dump()}}
    )
    return kfi

@router.get("/applicants/{applicant_id}/kfis/{kfi_id}", response_model=KeyFinancialIndicator)
async def get_kfi(applicant_id: str, kfi_id: str):
    db = get_db()
    kfi = db.key_financial_indicators.find_one({"_id": ObjectId(kfi_id), "is_deleted": {"$ne": True}})
    if kfi:
        kfi["id"] = str(kfi["_id"])
        return KeyFinancialIndicator(**kfi)
    raise HTTPException(status_code=404, detail="Key Financial Indicator not found")

@router.put("/applicants/{applicant_id}/kfis/{kfi_id}", response_model=KeyFinancialIndicator)
async def update_kfi(applicant_id: str, kfi_id: str, kfi: KeyFinancialIndicator):
    db = get_db()
    result = db.key_financial_indicators.update_one(
        {"_id": ObjectId(kfi_id)},
        {"$set": kfi.model_dump(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Key Financial Indicator not found")
    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$set": {"key_financial_indicators": kfi.model_dump()}}
    )
    return kfi

@router.delete("/applicants/{applicant_id}/kfis/{kfi_id}", status_code=200)
async def delete_kfi(applicant_id: str, kfi_id: str):
    db = get_db()
    result = db.key_financial_indicators.update_one(
        {"_id": ObjectId(kfi_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Key Financial Indicator not found")
    db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$unset": {"key_financial_indicators": 1}} # Changed from "" to 1
    )
    return {"message": "Key Financial Indicator soft deleted"}