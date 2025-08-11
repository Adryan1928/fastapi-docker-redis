from fastapi import FastAPI
from passlib.context import CryptContext
from utils import load_env
import os

load_env()

SECRET_KEY = os.getenv("SECRET_KEY")

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

app = FastAPI()

from auth.routes import router as auth_router
from orders.routes import router as orders_router

# Adicionando as rotas dos arquivos (parecido com o include do Django)
app.include_router(auth_router)
app.include_router(orders_router)
