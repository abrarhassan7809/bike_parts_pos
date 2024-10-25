# models.py
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime, Boolean
from sqlalchemy.orm import relationship
from db_config.db import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    token = Column(String, nullable=True)
    joined = Column(DateTime(timezone=True), default=datetime.utcnow, nullable=False)
    active = Column(Boolean, default=False)
    user_type = Column(Integer, nullable=True)


class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=True)
    barcode = Column(String, nullable=True)
    brand = Column(String, nullable=True)
    company = Column(String, nullable=True)
    rank_number = Column(String, nullable=True)
    pur_price = Column(Float, nullable=True)
    sel_price = Column(Float, nullable=False)
    quantity = Column(Integer, default=1, nullable=True)
    current_date = Column(String, nullable=True)


class Customer(Base):
    __tablename__ = "customer"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    phone_num = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    address = Column(String, nullable=True)


class Supplier(Base):
    __tablename__ = "supplier"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    company = Column(String(255), nullable=False)
    phon_num = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    address = Column(String(255), nullable=True)


class Invoice(Base):
    __tablename__ = "invoices"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    invoice_code = Column(String, nullable=True)
    customer_name = Column(String, nullable=True)
    walk_in_customer = Column(String, nullable=True)
    current_date = Column(String, nullable=False)
    grand_total = Column(Float, default=0.0, nullable=True)
    discount = Column(Float, default=0.0, nullable=True)
    receiving_amount = Column(Float, nullable=True)
    remaining_amount = Column(Float, nullable=True)

    invoice_with_item = relationship('InvoiceItem', back_populates='item_with_invoice', cascade="all, delete")


class InvoiceItem(Base):
    __tablename__ = "invoice_items"

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), default=1, nullable=False)
    product_code = Column(String(255), nullable=True)
    product_name = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    company = Column(String(255), nullable=True)
    quantity = Column(Integer, nullable=False)
    sell_price = Column(Float, nullable=False)
    total_price = Column(Float, nullable=False)

    item_with_invoice = relationship('Invoice', back_populates='invoice_with_item')
