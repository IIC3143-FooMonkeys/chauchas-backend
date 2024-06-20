from fastapi import APIRouter, HTTPException, status
from typing import List
from models.todos import Card
from schema.schema import cardEntity, cardEntities
from config.database import banksTable, cardsTable
from bson import ObjectId

router = APIRouter()

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
