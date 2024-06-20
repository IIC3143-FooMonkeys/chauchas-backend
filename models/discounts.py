from pydantic import BaseModel
import datetime as d

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
    paymentType: str
    bankName: str