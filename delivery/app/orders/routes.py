from fastapi import APIRouter, Depends
from utils import create_instance
from dependencies import get_session
from orders.models import Order
from sqlalchemy.orm import Session
from orders.schemas import OrderSchema

router = APIRouter(prefix="/orders", tags=["orders"])


@router.get("/")
async def read_orders():
    """
    Get a list of orders
    """
    return {"message": "List of orders"}

@router.post("/order")
async def create_order(order_schema: OrderSchema, session:Session = Depends(get_session)):
    """
    Create a new order
    """
    new_order = Order(**order_schema.model_dump())
    create_instance(session, new_order)

    return {"message": "Order created successfully", "order_id": new_order.id}
