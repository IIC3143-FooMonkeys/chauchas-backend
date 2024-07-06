from fastapi import APIRouter, HTTPException, status,Depends
from typing import List
from models.users import User
from schema.schema import userEntity, userEntities
from config.database import cardsTable, usersTable
from bson import ObjectId

router = APIRouter()

async def verify_user(userId: str):
    user_doc = usersTable.find_one({"auth0Id": str(userId)})
    if user_doc is None:
        raise HTTPException(status_code=400, detail="Invalid user")

    if user_doc["userType"] != 1:
        raise HTTPException(status_code=403, detail="User not authorized for this method")

    return user_doc

@router.get("/users", response_model=List[User])
async def get_users(page: int = 1, count: int = 25):
    offset = (page - 1) * count
    query = {}

    users = list(usersTable.find(query).skip(offset).limit(count))
    return userEntities(users)

@router.get("/users/{id}", response_model=User)
async def read_user(id: str):
    if (users := usersTable.find_one({"auth0Id": str(id)})) is not None:
        return userEntity(users)
    else:
        new_id = str(id) if id else str(ObjectId())
        data = {
            "_id": new_id,
            "auth0Id": id,
            "cards": [],
            "userType": 0
        }
        usersTable.insert_one(userEntity(data))
        newuser = usersTable.find_one({"auth0Id": str(id)})
        return userEntity(newuser)

@router.post("/users", response_model=User, status_code=status.HTTP_201_CREATED)
async def create_user(user: User, userId: str = Depends(verify_user)):
    user_dict = user.model_dump()
    usersTable.insert_one(userEntity(user_dict))
    return userEntity(user_dict)

@router.get("/users/{id}/cards", response_model=User)
async def read_user(id: str):
    if (user := usersTable.find_one({"auth0Id": str(id)})) is not None:
        if userEntity(user)["cards"] == []:
            raise HTTPException(status_code=404, detail=f"User with id {id} has no cards yet")
        return userEntity(user)
    raise HTTPException(status_code=400, detail=f"User with id {id} has not been registered yet")

@router.put("/users/{id}", response_model=User)
async def update_user(id: str, user: User, userId: str = Depends(verify_user)):
    if (user_before := usersTable.find_one({"auth0Id": str(id)})) is not None:
        usersTable.update_one({"auth0Id": str(id)}, {"$set": user.model_dump()})
        updated_user = usersTable.find_one({"_id": user_before["_id"]})
        return userEntity(updated_user)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.delete("/users/{id}", response_model=User)
async def delete_user(id: str, userId: str = Depends(verify_user)):
    if (user := usersTable.find_one({"auth0Id": str(id)})) is not None:
        usersTable.delete_one({"auth0Id": str(id)})
        return userEntity(user)
    raise HTTPException(status_code=404, detail=f"User with id {id} not found")

@router.put("/users/{userId}/add-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"auth0Id": str(userId)})) is not None:
        if (card := cardsTable.find_one({"_id": ObjectId(cardId)})) is not None:
            usersTable.update_one({"auth0Id": str(userId)}, {"$addToSet": {"cards": card}})
            updated_user = usersTable.find_one({"auth0Id": str(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"Card with id {cardId} not found")
    else:
        raise HTTPException(status_code=400, detail=f"User with id {userId} not found")
    
@router.put("/users/{userId}/delete-card/{cardId}", response_model=User)
async def add_card_to_user(userId: str, cardId: str):
    if (user := usersTable.find_one({"auth0Id": str(userId)})) is not None:
        card_found = False
        for card in user["cards"]:
            if str(card["_id"]) == str(cardId):
                card_found = True
                break
        if card_found:
            usersTable.update_one({"auth0Id": str(userId)}, {"$pull": {"cards": {"_id": ObjectId(cardId)}}})
            updated_user = usersTable.find_one({"auth0Id": str(userId)})
            return userEntity(updated_user)
        else:
            raise HTTPException(status_code=404, detail=f"User has no card with id {cardId}")
    else:
        raise HTTPException(status_code=400, detail=f"User with id {userId} not found")