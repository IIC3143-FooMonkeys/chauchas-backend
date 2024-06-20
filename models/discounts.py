from pydantic import BaseModel
import datetime as d

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
    card: str
    cardType: str
    bankName: str