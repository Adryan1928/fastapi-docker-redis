from fastapi import FastAPI
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from utils import load_env
import os

load_env()

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login-form")

app = FastAPI()

from auth.routes import router as auth_router
from orders.routes import router as orders_router

# Adicionando as rotas dos arquivos (parecido com o include do Django)
app.include_router(auth_router)
app.include_router(orders_router)


@app.get("/")
async def root():
    return {"message": "Welcome to the FastAPI application"}
