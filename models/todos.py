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
    name: str

class Card(BaseModel):
    bankId: str
    cardType: str
    bankName: str

class Category(BaseModel):
    name: str

class User(BaseModel):
    userId: str
    cards: list