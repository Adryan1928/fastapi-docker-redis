from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from database import Base


class Order(Base):
    __tablename__ = "orders"

    # STATUS_CHOICES = [
    #     ("PENDING", "Pending"),
    #     ("COMPLETED", "Completed"),
    #     ("CANCELED", "Canceled"),
    # ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    # status = Column(ChoiceType(STATUS_CHOICES), default="PENDING")
    status = Column(String, default="PENDING")
    user = Column(ForeignKey("users.id"))
    price = Column(Float)
    products = relationship("Product", cascade="all, delete")

    def __init__(self, user, price=0, status="PENDING"):
        self.user = user
        self.price = price
        self.status = status
        # self.product = product
    
    def calc_price(self):
        self.price = sum(product.price * product.quantity for product in self.products)


class Product(Base):
    __tablename__ = "products"

    # SIZE_CHOICES = [
    #     ("SMALL", "Small"),
    #     ("MEDIUM", "Medium"),
    #     ("LARGE", "Large"),
    # ]

    id = Column(Integer, primary_key=True, autoincrement=True)
    quantity = Column(Integer)
    flavor = Column(String)
    # size = Column(ChoiceType(SIZE_CHOICES), default="SMALL")
    size = Column(String)
    price = Column(Float)
    order = Column(ForeignKey("orders.id"))

    def __init__(self, price, quantity, size, flavor, order):
        self.price = price
        self.quantity = quantity
        self.size = size
        self.flavor = flavor
        self.order = order