def discountEntity(discount) -> dict:
    discount['id'] = str(discount['_id'])
    del discount['_id']
    return {
        "id": discount["id"],
        "url": str(discount["url"]),
        "title": str(discount["title"]),
        "discount": int(discount["discount"]),
        "description": str(discount["description"]),
        "category": str(discount["category"]),
        "expiration": discount["expiration"]
    }

def discountEntities(entity) -> list:
    return[discountEntity(discount) for discount in entity]