from config.database import banksTable, categoriesTable
from bson import ObjectId

def categoryEntity(category) -> dict:
    if '_id' in category:
        category['id'] = str(category['_id'])
        del category['_id']
    return {
        "id": category["id"],
        "name": str(category["name"])
    }

def discountEntity(discount) -> dict:
    if '_id' in discount:
        discount['id'] = str(discount['_id'])
        del discount['_id']
    cat = discount["category"]
    category = categoriesTable.find_one({"_id": ObjectId(cat)})
    if not category:
        raise ValueError(f"Category with id {cat} not found")
    return {
        "id": discount["id"],
        "url": str(discount["url"]),
        "local": str(discount["local"]),
        "discount": int(discount["discount"]),
        "description": str(discount["description"]),
        "category": str(discount["category"]),
        "expiration": discount["expiration"],
        "days": str(discount["days"]),
        "card": str(discount["card"])
    }

def bankEntity(bank) -> dict:
    if '_id' in bank:
        bank['id'] = str(bank['_id'])
        del bank['_id']
    return {
        "id": bank["id"],
        "name": str(bank["name"])
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
        "bankName": bank_data["name"],
        "paymentMethod": str(card["paymentMethod"])
    }

def userEntity(user) -> dict:
    formatted_cards = [cardEntity(card) for card in user["cards"]]

    return {
        "_id": str(user["auth0Id"]),
        "auth0Id": str(user["auth0Id"]),
        "cards": formatted_cards
    }

def discountEntities(entity) -> list:
    return[discountEntity(discount) for discount in entity]

def bankEntities(entity) -> list:
    return[bankEntity(bank) for bank in entity]

def cardEntities(entity) -> list:
    return[cardEntity(card) for card in entity]

def userEntities(entity) -> list:
    return[userEntity(user) for user in entity]

def categoryEntities(entity) -> list:
    return[categoryEntity(category) for category in entity]