from fastapi import APIRouter, HTTPException
from typing import List
from bson.objectid import ObjectId
from app.db import get_db
from app.models.applicant import Applicant

router = APIRouter()

@router.post("/applicants/", response_model=Applicant, status_code=201)
async def create_applicant(applicant: Applicant):
    db = get_db()
    result = db.applicants.insert_one(applicant.model_dump(exclude_unset=True))
    applicant.id = str(result.inserted_id)
    return applicant

@router.get("/applicants/", response_model=List[Applicant])
async def get_applicants():
    db = get_db()
    applicants = []
    for doc in db.applicants.find({"is_deleted": {"$ne": True}}):
        doc["id"] = str(doc["_id"])
        applicants.append(Applicant(**doc))
    return applicants

@router.get("/applicants/{applicant_id}", response_model=Applicant)
async def get_applicant(applicant_id: str):
    db = get_db()
    applicant = db.applicants.find_one({"_id": ObjectId(applicant_id), "is_deleted": {"$ne": True}})
    if applicant:
        applicant["id"] = str(applicant["_id"])
        return Applicant(**applicant)
    raise HTTPException(status_code=404, detail="Applicant not found")

@router.put("/applicants/{applicant_id}", response_model=Applicant)
async def update_applicant(applicant_id: str, applicant: Applicant):
    db = get_db()
    result = db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$set": applicant.model_dump(exclude_unset=True)}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return applicant

@router.delete("/applicants/{applicant_id}", status_code=200)
async def delete_applicant(applicant_id: str):
    db = get_db()
    result = db.applicants.update_one(
        {"_id": ObjectId(applicant_id)},
        {"$set": {"is_deleted": True}}
    )
    if result.modified_count == 0:
        raise HTTPException(status_code=404, detail="Applicant not found")
    return {"message": "Applicant soft deleted"}