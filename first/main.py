from fastapi import FastAPI
from pydantic import BaseModel

DB = []
next_id = 1

app = FastAPI()

class UserPayload(BaseModel):
    name: str
    email: str

class User(UserPayload):
    id: int

@app.get("/")
def home():
    return {"mensagem": "Olá, Mundo!"}

@app.get("/user/")
def get_users():
    return {"mensagem": "Obtendo informações do usuário...", "usuarios": DB}

@app.get("/user/{user_id}")
def get_user(user_id: int):
    user = next((u for u in DB if u.id == user_id), None)
    if user:
        return {"mensagem": "Usuário encontrado!", "usuario": user}
    return {"mensagem": "Usuário não encontrado!"}

@app.post("/user/")
def create_user(user: UserPayload):
    global next_id
    new_user = User(id=next_id, **user.model_dump())
    next_id += 1

    DB.append(new_user)

    return {"mensagem": "Usuário criado com sucesso!", "usuario": new_user}

@app.put("/user/{user_id}")
def update_user(user_id: int, user: UserPayload):
    existing_user_index = next(
            (i for i, u in enumerate(DB) if u.id == user_id), 
            None
        )
    if existing_user_index is not None:
        DB[existing_user_index].name = user.name
        DB[existing_user_index].email = user.email
        return {"mensagem": "Usuário atualizado com sucesso!", "usuario": DB[existing_user_index]}
    return {"mensagem": "Usuário não encontrado!"}

@app.delete("/user/{user_id}")
def delete_user(user_id: int):
    existing_user_index = next(
            (i for i, u in enumerate(DB) if u.id == user_id), 
            None
        )

    if existing_user_index is not None:
        DB.pop(existing_user_index)
        return {"mensagem": "Usuário deletado com sucesso!"}
    return {"mensagem": "Usuário não encontrado!"}