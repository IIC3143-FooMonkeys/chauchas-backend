from config.database import banksTable, categoriesTable
from bson import ObjectId

def categoryEntity(category) -> dict:
    if '_id' in category:
        category['id'] = str(category['_id'])
        del category['_id']
    return {
        "id": category["id"],
        "categoryName": str(category["categoryName"])
    }

def discountEntity(discount) -> dict:
    if '_id' in discount:
        discount['id'] = str(discount['_id'])
        del discount['_id']
    return {
        "id": discount["id"],
        "url": str(discount["url"]),
        "local": str(discount["local"]),
        "discount": int(discount["discount"]),
        "description": str(discount["description"]),
        "category": str(discount["category"]),
        "expiration": discount["expiration"],
        "days": str(discount["days"])
    }

def bankEntity(bank) -> dict:
    if '_id' in bank:
        bank['id'] = str(bank['_id'])
        del bank['_id']
    return {
        "id": bank["id"],
        "bankName": str(bank["bankName"])
    }

def cardEntity(card) -> dict:
    if '_id' in card:
        card['id'] = str(card['_id'])
        del card['_id']
    
    bank = banksTable.find_one({"_id": ObjectId(card["bankId"])})
    if not bank:
        raise ValueError(f"Bank with id {card['bankId']} not found")

    bank_data = bankEntity(bank)
    return {
        "id": card["id"],
        "bankId": bank_data["id"],
        "cardType": str(card["cardType"]),
        "bankName": bank_data["bankName"]
    }

def discountEntities(entity) -> list:
    return[discountEntity(discount) for discount in entity]