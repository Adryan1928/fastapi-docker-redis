from pydantic import BaseModel

class OrderSchema(BaseModel):
    user: int

    class Config:
        from_attributes = True