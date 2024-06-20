from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from models.todos import Discount, Bank, Card, Category, User
from schema.schema import discountEntity, discountEntities,cardEntity, \
    cardEntities,bankEntity, bankEntities,userEntity, userEntities, categoryEntity, categoryEntities
from config.database import discountsTable,categoriesTable,banksTable,cardsTable,categoriesTable,usersTable
from bson import ObjectId

router = APIRouter()

# ROUTES FOR CATEGORIES #

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

# ROUTES FOR DISCOUNTS #

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
    category_doc = categoriesTable.find_one({"categoryName": str(discount.category)})
    if category_doc is None:
        raise HTTPException(status_code=400, detail="Invalid category")
    discount_dict = discount.dict()
    discount_dict['category'] = str(category_doc["_id"])
    discount_dict['_id'] = ObjectId()
    discount_dict['id'] = ObjectId()
    new_discount = discountsTable.insert_one(discountEntity(discount_dict))
    return discountEntity(discount_dict)

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

# ROUTES FOR BANKS #

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

# ROUTES FOR CARDS #

@router.get("/cards", response_model=List[Card])
async def get_cards(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    cards = list(cardsTable.find(query).skip(offset).limit(count))
    return cardEntities(cards)

@router.get("/cards/{id}", response_model=Card)
async def read_card(id: str):
    if (cards := cardsTable.find_one({"_id": ObjectId(id)})) is not None:
        return cardEntity(cards)
    raise HTTPException(status_code=404, detail=f"Card with id {id} not found")

@router.get("/cards/by-bank", response_model=List[Card])
async def get_cards_by_bank(bankId: str, page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {"bankId": ObjectId(bankId)}

    cards = list(cardsTable.find(query).skip(offset).limit(count))
    if not cards:
        raise HTTPException(status_code=404, detail=f"No cards found for the bank {bankId}")
    return cardEntities(cards)

# ROUTES FOR USERS #

@router.get("/users", response_model=List[Card])
async def get_users(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    users = list(usersTable.find(query).skip(offset).limit(count))
    return userEntities(users)

@router.get("/users/{id}", response_model=User)
async def read_user(id: str):
    if (users := usersTable.find_one({"_id": ObjectId(id)})) is not None:
        return userEntity(users)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.get("/users/{id}/cards", response_model=List[Card])
async def get_cards_by_user(id: str, page: int = 1, count: int = 25):
    offset = (page - 1) * count
    user = usersTable.find_one({"_id": ObjectId(id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    cards = user.get("cards", [])
    formatted_cards = [cardEntity(card) for card in cards]
    return formatted_cards[offset:offset+count]