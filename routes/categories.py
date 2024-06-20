from fastapi import APIRouter, HTTPException, status
from typing import List
from models.todos import Category
from schema.schema import categoryEntity, categoryEntities
from config.database import categoriesTable, categoriesTable
from bson import ObjectId

router = APIRouter()

@router.get("/categories", response_model=List[Category])
async def get_categories(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    categories = list(categoriesTable.find(query).skip(offset).limit(count))
    return categoryEntities(categories)

@router.get("/categories/{id}", response_model=Category)
async def read_category(id: str):
    if (categories := categoriesTable.find_one({"_id": ObjectId(id)})) is not None:
        return categoryEntity(categories)
    raise HTTPException(status_code=404, detail=f"Category with id {id} not found")

@router.post("/categories", response_model=Category, status_code=status.HTTP_201_CREATED)
async def create_category(category: Category):
    category_dict = category.model_dump()
    category_dict['_id'] = ObjectId()
    category_dict['id'] = ObjectId()
    categoriesTable.insert_one(categoryEntity(category_dict))
    return categoryEntity(category_dict)

@router.put("/categories/{id}", response_model=Category)
async def update_category(id: str, category: Category):
    if categoriesTable.find_one({"_id": ObjectId(id)}) is not None:
        categoriesTable.update_one({"_id": ObjectId(id)}, {"$set": category.model_dump()})
        updated_category = categoriesTable.find_one({"_id": ObjectId(id)})
        return categoryEntity(updated_category)
    raise HTTPException(status_code=404, detail=f"Category with id {id} not found")

@router.delete("/categories/{id}", response_model=Category)
async def delete_category(id: str):
    if (category := categoriesTable.find_one({"_id": ObjectId(id)})) is not None:
        categoriesTable.delete_one({"_id": ObjectId(id)})
        return categoryEntity(category)
    raise HTTPException(status_code=404, detail=f"Category with id {id} not found")