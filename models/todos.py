from pydantic import BaseModel
import datetime as d
class Discount(BaseModel): #Modificar en base al E-R
    url: str
    title: str
    discount: int
    description: str
    category: str
    expiration: d.datetime
