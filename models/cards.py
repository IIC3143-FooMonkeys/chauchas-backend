from pydantic import BaseModel

class Card(BaseModel):
    id: str
    bankId: str
    cardType: str
    bankName: str
    paymentMethod: str