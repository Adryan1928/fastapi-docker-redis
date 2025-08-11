from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv

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

def get_session():
    try:
        from database import db
        Session = sessionmaker(bind=db)
        session_ = Session()
        yield session_
    finally:
        session_.close()
