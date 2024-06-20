from pydantic import BaseModel

class User(BaseModel):
    _id: str
    auth0Id: str
    cards: list