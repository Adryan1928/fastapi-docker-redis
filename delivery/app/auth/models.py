from sqlalchemy import Column, Integer, String, Boolean
from database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    email = Column(String, unique=True, nullable=False)
    password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)


    def __init__(self, name, email, password, is_active=True, is_admin=False):
        self.name = name
        self.email = email
        self.password = password
        self.is_active = is_active
        self.is_admin = is_admin
