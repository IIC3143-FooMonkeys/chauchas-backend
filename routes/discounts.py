from fastapi import APIRouter, HTTPException, Query, Depends
from typing import Optional, List
from models.discounts import Discount
from schema.schema import discountEntity, discountEntities
from config.database import discountsTable, usersTable
from bson import ObjectId

router = APIRouter()

async def verify_user(userId: str):
    user_doc = usersTable.find_one({"auth0Id": str(userId)})
    if user_doc is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    if user_doc["userType"] != 1:
        raise HTTPException(status_code=403, detail="User not authorized for this method")

    return user_doc

@router.get("/discounts", response_model=List[Discount])
async def get_discounts(
        page: int = 1,
        count: int = 25,
        category: Optional[str] = Query(None, description="Category ID to filter discounts"),
        cardType: Optional[str] = Query(None, description="Card Type to filter discounts"),
        bankName: Optional[str] = Query(None, description="Bank Name to filter discounts"),
        paymentMethod: Optional[str] = Query(None, description="Payment Method to filter discounts")
    ):
    offset = (page - 1) * count
    query = {}

    if category:
        query["category"] = category
    if cardType:
        query["cardType"] = cardType
    if bankName:
        query["bankName"] = bankName
    if paymentMethod:
        query["paymentMethod"] = paymentMethod

    discounts = list(discountsTable.find(query).skip(offset).limit(count))
    return discountEntities(discounts)

@router.get("/discounts/{id}", response_model=Discount)
async def read_discount(id: str):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.put("/discounts/{id}", response_model=Discount)
async def update_discount(id: str, discount: Discount, userId: str = Depends(verify_user)):
    if discountsTable.find_one({"_id": ObjectId(id)}) is not None:
        discountsTable.update_one({"_id": ObjectId(id)}, {"$set": discount.model_dump()})
        updated_discount = discountsTable.find_one({"_id": ObjectId(id)})
        return discountEntity(updated_discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.delete("/discounts/{id}", response_model=Discount)
async def delete_discount(id: str, userId: str = Depends(verify_user)):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        discountsTable.delete_one({"_id": ObjectId(id)})
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")