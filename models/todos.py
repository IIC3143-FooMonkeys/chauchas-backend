from pydantic import BaseModel

class Discount(BaseModel): #Modificar en base al E-R
    name: str
    category: str
