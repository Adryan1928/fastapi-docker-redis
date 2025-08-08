from typing import List, Optional
from sqlmodel import Session, select
from .models import User, UserCreate

def create_user(session: Session, user_in: UserCreate) -> User:
    db_user = User(**user_in.model_dump())
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return db_user

def get_users(session: Session) -> List[User]:
    return session.exec(select(User)).all()

def get_user(session: Session, user_id: int) -> Optional[User]:
    return session.get(User, user_id)
