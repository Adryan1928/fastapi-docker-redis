from typing import Optional
from sqlmodel import SQLModel, Field

class UserBase(SQLModel):
    name: str
    email: str

class User(UserBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)

class UserCreate(UserBase):
    pass
