from pydantic import BaseModel
import datetime as d
class Discount(BaseModel): #Modificar en base al E-R
    name: str
    category: str
    url: str
    title: str
    discount: int
    description: str
    expiration: d.datetime
