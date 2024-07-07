from pydantic import BaseModel
import datetime as d

class Discount(BaseModel):
    id: str
    url: str
    imageUrl: str
    local: str
    discount: int
    description: str
    category: str
    expiration: d.datetime
    days: str
    card: str
    cardType: str
    paymentMethod: str
    bankName: str