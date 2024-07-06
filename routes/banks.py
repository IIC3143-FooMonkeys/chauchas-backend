from fastapi import APIRouter, HTTPException, status, Depends
from typing import List
from models.banks import Bank
from schema.schema import bankEntity, bankEntities
from config.database import banksTable, usersTable
from bson import ObjectId

router = APIRouter()

async def verify_user(userId: str):
    user_doc = usersTable.find_one({"auth0Id": str(userId)})
    if user_doc is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    if user_doc["userType"] != 1:
        raise HTTPException(status_code=403, detail="User not authorized for this method")

    return user_doc

@router.get("/banks", response_model=List[Bank])
async def get_banks(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    banks = list(banksTable.find(query).skip(offset).limit(count))
    return bankEntities(banks)

@router.get("/banks/{id}", response_model=Bank)
async def read_bank(id: str):
    if (banks := banksTable.find_one({"id": id})) is not None:
        return bankEntity(banks)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")

@router.post("/banks", response_model=Bank, status_code=status.HTTP_201_CREATED)
async def create_bank(bank: Bank, userId: str = Depends(verify_user)):
    bank_dict = bank.model_dump()
    bank_dict['_id'] = ObjectId()
    bank_dict['id'] = ObjectId()
    banksTable.insert_one(bankEntity(bank_dict))
    return bankEntity(bank_dict)

@router.put("/banks/{id}", response_model=Bank)
async def update_bank(id: str, bank: Bank, userId: str = Depends(verify_user)):
    if banksTable.find_one({"id": id}) is not None:
        banksTable.update_one({"id": id}, {"$set": bank.model_dump()})
        updated_bank = banksTable.find_one({"id": id})
        return bankEntity(updated_bank)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")

@router.delete("/banks/{id}", response_model=Bank)
async def delete_bank(id: str, userId: str = Depends(verify_user)):
    if (bank := banksTable.find_one({"id": id})) is not None:
        banksTable.delete_one({"id": id})
        return bankEntity(bank)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")
