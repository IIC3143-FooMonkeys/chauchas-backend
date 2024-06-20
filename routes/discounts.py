from fastapi import APIRouter, HTTPException, Query
from typing import Optional, List
from models.todos import Discount
from schema.schema import discountEntity, discountEntities
from config.database import discountsTable
from bson import ObjectId

router = APIRouter()


@router.get("/discounts", response_model=List[Discount])
async def get_discounts(
        page: int = 1,
        count: int = 25,
        category: Optional[str] = Query(None, description="Category ID to filter discounts")
):
    offset = (page - 1) * count
    query = {}

    if category:
        query["category"] = category

    discounts = list(discountsTable.find(query).skip(offset).limit(count))
    return discountEntities(discounts)
@router.get("/discounts/{id}", response_model=Discount)
async def read_discount(id: str):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.put("/discounts/{id}", response_model=Discount)
async def update_discount(id: str, discount: Discount):
    if discountsTable.find_one({"_id": ObjectId(id)}) is not None:
        discountsTable.update_one({"_id": ObjectId(id)}, {"$set": discount.model_dump()})
        updated_discount = discountsTable.find_one({"_id": ObjectId(id)})
        return discountEntity(updated_discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.delete("/discounts/{id}", response_model=Discount)
async def delete_discount(id: str):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        discountsTable.delete_one({"_id": ObjectId(id)})
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")