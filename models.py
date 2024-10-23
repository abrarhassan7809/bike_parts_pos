# models.py
from sqlalchemy import Column, Integer, String, Float
from db import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    barcode = Column(String, nullable=False)
    pur_price = Column(Float, nullable=False)
    sel_price = Column(Float, nullable=False)
    quantity = Column(Integer, nullable=False)
