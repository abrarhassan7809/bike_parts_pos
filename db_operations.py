#db_operations.py
from models import Product
from db import SessionLocal
session = SessionLocal()


def insert_product(name, price, quantity):
    product = Product(name=name, price=price, quantity=quantity)
    session.add(product)
    session.commit()

def update_product(product_id, name=None, price=None, quantity=None):
    product = session.query(Product).filter_by(id=product_id).first()
    if name:
        product.name = name
    if price:
        product.price = price
    if quantity:
        product.quantity = quantity
    session.commit()

def delete_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    session.delete(product)
    session.commit()

def get_all_products():
    return session.query(Product).all()
