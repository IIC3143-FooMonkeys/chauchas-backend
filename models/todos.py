from pydantic import BaseModel
import datetime as d
class Discount(BaseModel): #Modificar en base al E-R
    id: str
    url: str
    local: str
    discount: int
    description: str
    category: str
    expiration: d.datetime
    days: str
    card: str

class Bank(BaseModel):
    id: str
    name: str

class Card(BaseModel):
    id: str
    bankId: str
    cardType: str
    bankName: str
    paymentMethod: str

class Category(BaseModel):
    id: str
    name: str

class User(BaseModel):
    _id: str
    auth0Id: str
    cards: list