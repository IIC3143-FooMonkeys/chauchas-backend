from pydantic import BaseModel
import datetime as d
class Bank(BaseModel):
    id: str
    name: str

class Card(BaseModel):
    id: str
    bankId: str
    cardType: str
    bankName: str
    paymentMethod: str

class Discount(BaseModel):
    id: str
    url: str
    local: str
    discount: int
    description: str
    category: str
    expiration: d.datetime
    days: str
    card: Card

class Category(BaseModel):
    id: str
    name: str

class User(BaseModel):
    _id: str
    auth0Id: str
    cards: list