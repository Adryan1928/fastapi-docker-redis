from fastapi import FastAPI

app = FastAPI()

from auth.routes import router as auth_router
from orders.routes import router as orders_router

# Adicionando as rotas dos arquivos (parecido com o include do Django)
app.include_router(auth_router)
app.include_router(orders_router)
