from fastapi import APIRouter, HTTPException, status
from typing import Optional, List
from models.todos import Discount, Bank, Card, Category, User
from schema.schema import discountEntity, discountEntities,cardEntity, \
    cardEntities,bankEntity, bankEntities,userEntity, userEntities, categoryEntity, categoryEntities
from config.database import discountsTable,categoriesTable,banksTable,cardsTable,categoriesTable,usersTable
from bson import ObjectId

router = APIRouter()

@router.get("/")
def read_root():
    return {"message": "Hello World"}

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

@router.post("/cards", response_model=Card, status_code=status.HTTP_201_CREATED)
async def create_card(card: Card):
    bank_doc = banksTable.find_one({"name": str(card.bankName)})
    if bank_doc is None:
        raise HTTPException(status_code=400, detail="Invalid bank")
    card_dict = card.model_dump()
    card_dict['bankId'] = str(bank_doc["_id"])
    card_dict['_id'] = ObjectId()
    card_dict['id'] = ObjectId()
    cardsTable.insert_one(cardEntity(card_dict))
    return cardEntity(card_dict)

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
    if (users := usersTable.find_one({"_id": str(id)})) is not None:
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
    usersTable.insert_one(userEntity(user_dict))
    return userEntity(user_dict)

@router.get("/users/{id}/cards", response_model=User)
async def read_user(id: str):
    if (user := usersTable.find_one({"_id": str(id)})) is not None:
        return userEntity(user)
    raise HTTPException(status_code=404, detail=f"User with id {id} has no cards yet")

@router.put("/users/{id}", response_model=User)
async def update_user(id: str, user: User):
    if usersTable.find_one({"_id": str(id)}) is not None:
        usersTable.update_one({"_id": str(id)}, {"$set": user.model_dump()})
        updated_user = usersTable.find_one({"_id": str(id)})
        return userEntity(updated_user)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.put("/users/{userId}/add-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"_id": str(userId)})) is not None:
        if (card := cardsTable.find_one({"_id": ObjectId(cardId)})) is not None:
            usersTable.update_one({"_id": str(userId)}, {"$addToSet": {"cards": card}})
            updated_user = usersTable.find_one({"_id": str(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"Card with id {cardId} not found")
    else:
        raise HTTPException(status_code=404, detail=f"User with id {userId} not found")
    
@router.put("/users/{userId}/delete-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"_id": str(userId)})) is not None:
        card_found = False
        for card in user["cards"]:
            if str(card["_id"]) == str(cardId):
                card_found = True
                break
        if card_found:
            usersTable.update_one({"_id": str(userId)}, {"$pull": {"cards": {"_id": ObjectId(cardId)}}})
            updated_user = usersTable.find_one({"_id": str(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"User has no card with id {cardId}")
    else:
        raise HTTPException(status_code=404, detail=f"User with id {userId} not found")