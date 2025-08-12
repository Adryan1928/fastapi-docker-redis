from fastapi import Depends, HTTPException
from sqlalchemy.orm import sessionmaker, Session
from auth.models import User
from database import db
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM, oauth2_scheme

def get_session():
    try:
        Session = sessionmaker(bind=db)
        session_ = Session()
        yield session_
    finally:
        session_.close()


def verify_token(token: str = Depends(oauth2_scheme), session:Session = Depends(get_session)):
    try:
        dic_info = jwt.decode(token, SECRET_KEY, ALGORITHM)
        user_id = int(dic_info.get("sub"))
    except JWTError:
        raise HTTPException(status_code=401, detail="Invalid token or expired")

    user = session.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    return user