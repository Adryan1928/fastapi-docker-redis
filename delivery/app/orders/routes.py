from fastapi import APIRouter, Depends, HTTPException
from utils import create_instance
from dependencies import get_session, verify_token
from orders.models import Order, Product
from auth.models import User
from sqlalchemy.orm import Session
from orders.schemas import OrderSchema, ProductSchema, ResponseOrderSchema
from typing import List

router = APIRouter(prefix="/orders", tags=["orders"], dependencies=[Depends(verify_token)])


@router.get("/", response_model=List[ResponseOrderSchema])
async def read_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):

    orders = session.query(Order).filter(Order.user == user.id).all()
    return orders

@router.post("/order")
async def create_order(order_schema: OrderSchema, session:Session = Depends(get_session)):
    """
    Create a new order
    """
    new_order = Order(**order_schema.model_dump())
    create_instance(session, new_order)

    return {"message": "Order created successfully", "order_id": new_order.id}

@router.get("/order/{id_order}", response_model=ResponseOrderSchema)
async def get_order(id_order: int, session:Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Get a order
    """

    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if not user.is_admin and order.user != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to access this order")

    return {
        "qnt_products": len(order.products),
        "order": order
    }


@router.post("/order/cancel/{id_order}")
async def cancel_order(id_order: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Cancel an existing order
    """
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_admin and order.user != user:
        raise HTTPException(status_code=403, detail="Not authorized to cancel this order")

    order.status = "CANCELED"
    session.commit()
    return {
            "message": f"Order({order.id}) canceled successfully",
            "order": order,
        }

@router.post("/order/finish/{id_order}")
async def finish_order(id_order: int, session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    Finish an existing order
    """
    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_admin and order.user != user:
        raise HTTPException(status_code=403, detail="Not authorized to finish this order")

    order.status = "FINISHED"
    session.commit()
    return {
            "message": f"Order({order.id}) finished successfully",
            "order": order,
        }


@router.get("/list")
async def list_orders(session: Session = Depends(get_session), user: User = Depends(verify_token)):
    """
    List all orders
    """
    if not user.is_admin:
        raise HTTPException(status_code=403, detail="Not authorized to list orders")
    
    orders = session.query(Order).all()
    return {"orders": orders}


@router.post("/order/add-product/{id_order}")
async def add_product_to_order(
        id_order: int,
        product_schema: ProductSchema,
        session: Session = Depends(get_session),
        user: User = Depends(verify_token)
    ):

    """
    Add a product to an existing order
    """

    order = session.query(Order).filter(Order.id == id_order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_admin and order.user != user:
        raise HTTPException(status_code=403, detail="Not authorized to add products to this order")

    product = Product(**product_schema.model_dump(), order=order.id)
    create_instance(session, product)
    order.calc_price()
    session.commit()

    return {
        "message": f"Product added to order({order.id}) successfully",
        "order": order,
        "product_id": product.id,
    }


@router.post("/order/remove-product/{id_product}")
async def remove_product_from_order(
        id_product: int,
        session: Session = Depends(get_session),
        user: User = Depends(verify_token)
    ):

    """
    Remove a product from an existing order
    """

    product = session.query(Product).filter(Product.id == id_product).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    order = session.query(Order).filter(Order.id == product.order).first()
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")

    if not user.is_admin and order.user != user:
        raise HTTPException(status_code=403, detail="Not authorized to remove products from this order")

    session.delete(product)
    session.commit()
    order.calc_price()
    session.commit()

    return {
        "message": f"Product removed from order({order.id}) successfully",
        "order": order,
        "products": order.products,
    }