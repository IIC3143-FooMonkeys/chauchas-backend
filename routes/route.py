from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from models.todos import Discount
from schema.schema import discountEntity, discountEntities
from config.database import discountsTable
from bson import ObjectId

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello World"}

@router.get("/discounts", response_model=List[Discount])
async def get_discounts(page: int = 1, count: int = 25, category: Optional[str] = None):
    offset = (page - 1) * count
    query = {}
    if category:
        query["category"] = category

    discounts = list(discountsTable.find(query).skip(offset).limit(count))
    return discountEntities(discounts)

@router.get("/discounts/{id}", response_model=Discount)
async def read_discount(id: str):
    if (discount := discountsTable.find_one({"id": ObjectId(id)})) is not None:
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.put("/discounts/{id}", response_model=Discount)
async def update_discount(id: str, discount: Discount):
    if discountsTable.find_one({"id": ObjectId(id)}) is not None:
        discountsTable.update_one({"id": ObjectId(id)}, {"$set": discountEntity(discount)})
        updated_discount = discountsTable.find_one({"id": ObjectId(id)})
        return discountEntity(updated_discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.delete("/discounts/{id}", response_model=Discount)
async def delete_discount(id: str):
    if (discount := discountsTable.find_one({"id": ObjectId(id)})) is not None:
        discountsTable.delete_one({"id": ObjectId(id)})
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")