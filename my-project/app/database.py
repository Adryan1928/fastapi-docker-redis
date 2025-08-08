import os
import time
from sqlmodel import SQLModel, create_engine, Session
from sqlalchemy.exc import OperationalError

DATABASE_URL = os.getenv("DATABASE_URL")
# para debug no SQL: echo=True
engine = create_engine(DATABASE_URL, echo=True)

def init_db(retries: int = 10, wait: float = 1.0):
    """
    Tenta criar as tabelas; faz retry para esperar o Postgres subir.
    Bom para desenvolvimento via docker-compose.
    """
    for attempt in range(1, retries + 1):
        try:
            SQLModel.metadata.create_all(engine)
            print("Database ready and tables created")
            return
        except OperationalError as ex:
            print(f"DB not ready (attempt {attempt}/{retries}) - retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("Could not initialize the database after retries")

def get_session():
    with Session(engine) as session:
        yield session
