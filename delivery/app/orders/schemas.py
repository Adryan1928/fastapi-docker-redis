from pydantic import BaseModel
from typing import List

class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True


class ProductSchema(BaseModel):
    quantity: int
    flavor: str
    size: str
    price: float

    class Config:
        from_attributes = True


class ResponseOrderSchema(BaseModel):
    id: int
    price: float
    status: str
    products: List[ProductSchema]

    class Config:
        from_attributes = True