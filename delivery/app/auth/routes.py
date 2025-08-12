from datetime import timedelta
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from auth.schemas import LoginSchema, UserSchema
from utils import authenticate_user, create_instance, create_token
from dependencies import get_session, verify_token
from auth.models import User
from main import bcrypt_context
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def auth_root():
    """
    Root endpoint for authentication
    """
    return {"message": "Auth root"}

@router.post("/registration")
async def register_user(user_schema: UserSchema, session: Session = Depends(get_session)):
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
    
@router.post("/login")
async def login(login_schema: LoginSchema, session: Session = Depends(get_session)):
    user = authenticate_user(login_schema.email, login_schema.password, session)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password | User not found")

    access_token = create_token(user.id)
    refresh_token = create_token(user.id, timedelta(days=7))

    return {
            "message": "Login successful",
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }

@router.post("/login-form")
async def login_form(form: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(get_session)):
    user = authenticate_user(form.username, form.password, session)

    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password | User not found")

    access_token = create_token(user.id)

    return {
            "access_token": access_token,
            "token_type": "bearer"
        }

@router.get("/refresh")
async def refresh_token(user: User = Depends(verify_token)):
    access_token = create_token(user.id)

    return {
        "message": "Token refreshed successfully",
        "access_token": access_token,
        "token_type": "bearer"
    }