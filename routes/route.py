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