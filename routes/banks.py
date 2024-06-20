from fastapi import APIRouter, HTTPException, status
from typing import List
from models.banks import Bank
from schema.schema import bankEntity, bankEntities
from config.database import banksTable
from bson import ObjectId

router = APIRouter()

@router.get("/banks", response_model=List[Bank])
async def get_banks(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    banks = list(banksTable.find(query).skip(offset).limit(count))
    return bankEntities(banks)

@router.get("/banks/{id}", response_model=Bank)
async def read_bank(id: str):
    if (banks := banksTable.find_one({"_id": ObjectId(id)})) is not None:
        return bankEntity(banks)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")

@router.post("/banks", response_model=Bank, status_code=status.HTTP_201_CREATED)
async def create_bank(bank: Bank):
    bank_dict = bank.model_dump()
    bank_dict['_id'] = ObjectId()
    bank_dict['id'] = ObjectId()
    banksTable.insert_one(bankEntity(bank_dict))
    return bankEntity(bank_dict)

@router.put("/banks/{id}", response_model=Bank)
async def update_bank(id: str, bank: Bank):
    if banksTable.find_one({"_id": ObjectId(id)}) is not None:
        banksTable.update_one({"_id": ObjectId(id)}, {"$set": bank.model_dump()})
        updated_bank = banksTable.find_one({"_id": ObjectId(id)})
        return bankEntity(updated_bank)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")

@router.delete("/banks/{id}", response_model=Bank)
async def delete_bank(id: str):
    if (bank := banksTable.find_one({"_id": ObjectId(id)})) is not None:
        banksTable.delete_one({"_id": ObjectId(id)})
        return bankEntity(bank)
    raise HTTPException(status_code=404, detail=f"Bank with id {id} not found")
