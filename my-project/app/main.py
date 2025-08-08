from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session
from .database import init_db, get_session
from .models import User, UserCreate
from contextlib import asynccontextmanager
from .crud import create_user as crud_create_user, get_users as crud_get_users, get_user as crud_get_user
import os

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield

app = FastAPI(title="Exemplo FastAPI + Postgres", lifespan=lifespan)

@app.get("/")
def read_root():
    name = os.getenv("APP_NAME", "unknown")
    return {"message": f"instância: {name}"}

@app.post("/users/", response_model=User)
def create_user(user: UserCreate, session: Session = Depends(get_session)):
    return crud_create_user(session, user)


@app.get("/users/", response_model=List[User])
def list_users(session: Session = Depends(get_session)):
    return crud_get_users(session)

@app.get("/users/{user_id}", response_model=User)
def read_user(user_id: int, session: Session = Depends(get_session)):
    db_user = crud_get_user(session, user_id)
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
