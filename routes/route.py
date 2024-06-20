from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from models.todos import Discount
from schema.schema import discountEntity, discountEntities
from config.database import discountsTable,categoriesTable
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



@router.post("/discounts", response_model=Discount, status_code=status.HTTP_201_CREATED)
async def create_discount(discount: Discount):
    # Convertir Discount a diccionario
    discount_dict = discount.dict(by_alias=True)
    discount_dict["id"] = ObjectId()
    # Buscar el ID de la categoría en la base de datos
    category_doc = categoriesTable.find_one({"categoryName": discount.category})
    if category_doc is None:
        raise HTTPException(status_code=400, detail="Invalid category")

    discount_dict["category"] = str(category_doc["_id"])

    # Insertar en la base de datos
    new_discount = discountsTable.insert_one(discount_dict)
    created_discount = discountsTable.find_one({"_id": new_discount.inserted_id})

    if created_discount is None:
        raise HTTPException(status_code=404, detail="Discount not found")

@router.get("/discounts/{id}", response_model=Discount)
async def read_discount(id: str):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.put("/discounts/{id}", response_model=Discount)
async def update_discount(id: str, discount: Discount):
    if discountsTable.find_one({"_id": ObjectId(id)}) is not None:
        discountsTable.update_one({"_id": ObjectId(id)}, {"$set": discountEntity(discount)})
        updated_discount = discountsTable.find_one({"_id": ObjectId(id)})
        return discountEntity(updated_discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")

@router.delete("/discounts/{id}", response_model=Discount)
async def delete_discount(id: str):
    if (discount := discountsTable.find_one({"_id": ObjectId(id)})) is not None:
        discountsTable.delete_one({"_id": ObjectId(id)})
        return discountEntity(discount)
    raise HTTPException(status_code=404, detail=f"Discount with id {id} not found")