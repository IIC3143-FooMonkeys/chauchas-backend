from pydantic import BaseModel

class Bank(BaseModel):
    id: str
    name: str