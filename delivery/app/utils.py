from sqlalchemy.orm import Session
import os
from dotenv import load_dotenv
from jose import jwt
from datetime import datetime, timedelta, timezone

def load_env():
    try:
        BASE_DIR = os.path.dirname(os.path.abspath(__file__))
        dotenv_path = os.path.join(BASE_DIR, "../.env")

        load_dotenv(dotenv_path=dotenv_path)
    except:
        load_dotenv()

def create_instance(session: Session, obj):
    """
    Create a new instance of a SQLAlchemy model and add it to the session.
    """
    session.add(obj)
    session.commit()

def create_token(id:int, duration_token:int = None):
    from main import ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, SECRET_KEY
    if not duration_token:
        duration_token = timedelta(minutes=int(ACCESS_TOKEN_EXPIRE_MINUTES))

    date_experitation = datetime.now(timezone.utc) + duration_token

    dic_info = {
        "sub": str(id),
        "exp": date_experitation
    }

    jwt_token = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_token

def authenticate_user(email:str, password:str, session:Session):
    from auth.models import User
    from main import bcrypt_context
    user = session.query(User).filter(User.email == email).first()
    if not user:
        return False
    elif not bcrypt_context.verify(password, user.password):
        return False
    
    return user