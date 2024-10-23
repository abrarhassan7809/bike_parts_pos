# db_operations.py
from models import Product
from db import SessionLocal
session = SessionLocal()

def insert_product(name, barcode, pur_price, sel_price, quantity):
    product = Product(name=name, barcode=barcode, pur_price=pur_price, sel_price=sel_price, quantity=quantity)
    session.add(product)
    session.commit()

def update_product(product_id, name=None, barcode=None, pur_price=None, sel_price=None, quantity=None):
    product = session.query(Product).filter_by(id=product_id).first()
    if name:
        product.name = name
    if barcode:
        product.barcode = barcode
    if pur_price:
        product.pur_price = pur_price
    if sel_price:
        product.sel_price = sel_price
    if quantity:
        product.quantity = quantity
    session.commit()

def delete_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    session.delete(product)
    session.commit()

def get_all_products():
    products = session.query(Product).all()
    return products

def get_product_by_barcode(barcode):
    return session.query(Product).filter_by(barcode=barcode).first()
