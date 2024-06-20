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
    category_doc = categoriesTable.find_one({"name": str(discount.category)})
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

# TO-DO POST

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

# TO-DO POST

@router.put("/cards/{id}", response_model=Card)
async def update_card(id: str, card: Card):
    if cardsTable.find_one({"_id": ObjectId(id)}) is not None:
        cardsTable.update_one({"_id": ObjectId(id)}, {"$set": card.model_dump()})
        updated_card = cardsTable.find_one({"_id": ObjectId(id)})
        return cardEntity(updated_card)
    raise HTTPException(status_code=404, detail=f"Card with id {id} not found")

@router.delete("/cards/{id}", response_model=Card)
async def delete_card(id: str):
    if (card := cardsTable.find_one({"_id": ObjectId(id)})) is not None:
        cardsTable.delete_one({"_id": ObjectId(id)})
        return cardEntity(card)
    raise HTTPException(status_code=404, detail=f"Card with id {id} not found")

# ROUTES FOR USERS #

@router.get("/users", response_model=List[User])
async def get_users(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    users = list(usersTable.find(query).skip(offset).limit(count))
    return userEntities(users)

@router.get("/users/{id}", response_model=User)
async def read_user(id: str):
    if (users := usersTable.find_one({"_id": ObjectId(id)})) is not None:
        return userEntity(users)
    else:
        data = {
            "userId": id,
            "auth0Id": "",
            "cards": []
        }
        usersTable.insert_one(userEntity(data))

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User):
    user_dict = user.model_dump()
    user_dict['_id'] = ObjectId()
    user_dict['id'] = ObjectId()
    usersTable.insert_one(userEntity(user_dict))
    return userEntity(user_dict)

@router.get("/users/{id}/cards", response_model=User)
async def read_user(id: str):
    if (user := usersTable.find_one({"_id": ObjectId(id)})) is not None:
        return userEntity(user)
    raise HTTPException(status_code=404, detail=f"User with id {id} has no cards yet")

@router.put("/users/{id}", response_model=User)
async def update_user(id: str, user: User):
    if usersTable.find_one({"_id": ObjectId(id)}) is not None:
        usersTable.update_one({"_id": ObjectId(id)}, {"$set": user.model_dump()})
        updated_user = usersTable.find_one({"_id": ObjectId(id)})
        return userEntity(updated_user)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.put("/users/{userId}/add-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"_id": ObjectId(userId)})) is not None:
        if (card := cardsTable.find_one({"_id": ObjectId(cardId)})) is not None:
            usersTable.update_one({"_id": ObjectId(userId)}, {"$addToSet": {"cards": card}})
            updated_user = usersTable.find_one({"_id": ObjectId(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"Card with id {cardId} not found")
    else:
        raise HTTPException(status_code=404, detail=f"User with id {userId} not found")
    
@router.put("/users/{userId}/delete-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"_id": ObjectId(userId)})) is not None:
        if (card := usersTable.find_one({"_id": ObjectId(cardId), "cards._id": ObjectId(cardId)})) is not None:
            usersTable.update_one({"_id": ObjectId(userId)}, {"$pull": {"cards": {"_id": ObjectId(cardId)}}})
            updated_user = usersTable.find_one({"_id": ObjectId(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"User has no card with id {cardId}")
    else:
        raise HTTPException(status_code=404, detail=f"User with id {userId} not found")