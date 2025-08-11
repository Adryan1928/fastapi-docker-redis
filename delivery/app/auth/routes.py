from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from delivery.app.auth.schemas import UserSchema
from utils import create_instance, get_session
from auth.models import User
from main import bcrypt_context

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def auth_root():
    """
    Root endpoint for authentication
    """
    return {"message": "Auth root"}

@router.post("/registration")
async def register_user(user_schema:UserSchema, session:Session = Depends(get_session)):
    """
    Endpoint for user registration
    """

    user = session.query(User).filter(User.email == user_schema.email).first()

    if (user):
        raise HTTPException(status_code=400, detail="User already exists")
    else:
        encrypted_password = bcrypt_context.hash(user_schema.password)
        user = User(name=user_schema.name, email=user_schema.email, password=encrypted_password, is_active=user_schema.is_active, is_admin=user_schema.is_admin)
        create_instance(session, user)
        return {"message": "User registered successfully"}