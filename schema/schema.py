def discountEntity(discount) -> dict:
    discount['id'] = str(discount['_id'])
    del discount['_id']
    return {
        "id": discount["id"],
        "name": str(discount["name"]),
        "category": str(discount["category"])
    }

def discountEntities(entity) -> list:
    return[discountEntity(discount) for discount in entity]