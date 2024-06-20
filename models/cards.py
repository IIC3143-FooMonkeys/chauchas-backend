from pydantic import BaseModel
import datetime as d

class Card(BaseModel):
    id: str
    bankId: str
    cardType: str
    bankName: str
    paymentMethod: str