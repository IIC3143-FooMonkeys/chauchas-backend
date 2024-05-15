from fastapi import APIRouter
from typing import Optional
from models.todos import Discount
from schema.schema import discountEntity, discountEntities
from config.database import discountsTable

router = APIRouter()

@router.get("/hello", response_model=list[Discount])
async def get_discounts(page: int = 1, count: int = 25, category: Optional[str] = None):
    offset = (page - 1) * count
    query = {}
    if category:
        query["category"] = category

    discounts = list(discountsTable.find(query).skip(offset).limit(count))
    return discountEntities(discounts)