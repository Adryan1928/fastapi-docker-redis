from fastapi import APIRouter

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
async def read_orders():
    """
    Get a list of orders
    """
    return {"message": "List of orders"}
