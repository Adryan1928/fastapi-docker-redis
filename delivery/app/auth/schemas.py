from pydantic import BaseModel
from typing import Optional

class UserSchema(BaseModel):
    name: str
    email: str
    password: str
    is_active: Optional[bool]
    is_admin: Optional[bool]

    class Config:
        from_attributes = True