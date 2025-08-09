from fastapi import APIRouter

router = APIRouter(prefix="/auth", tags=["auth"])

@router.get("/")
async def auth_root():
    """
    Root endpoint for authentication
    """
    return {"message": "Auth root"}