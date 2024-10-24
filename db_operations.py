# db_operations.py
from models import Product, Invoice, InvoiceItem
from db import SessionLocal
session = SessionLocal()

def insert_product(name, barcode, brand, company, rank_number, pur_price, sel_price, quantity):
    product = Product(name=name, barcode=barcode, brand=brand, company=company, rank_number=rank_number,
                      pur_price=pur_price, sel_price=sel_price, quantity=quantity)
    session.add(product)
    session.commit()

def update_product(product_id, name=None, barcode=None, brand=None, company=None, rank_number=None, pur_price=None,
                   sel_price=None, quantity=None):
    product = session.query(Product).filter_by(id=product_id).first()
    if name:
        product.name = name
    if barcode:
        product.barcode = barcode
    if brand:
        product.brand = brand
    if company:
        product.company = company
    if rank_number:
        product.rank_number = rank_number
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

def get_all_invoices():
    products = session.query(Invoice).all()
    return products

def get_invoice_by_id(invoice_id):
    invoice = session.query(Invoice).filter_by(id=invoice_id).first()
    if invoice:
        invoice.invoice_with_item = session.query(InvoiceItem).filter_by(invoice_id=invoice_id).all()
    return invoice


def get_product_by_barcode(barcode):
    products = session.query(Product).filter_by(barcode=barcode).first()
    return products

def get_product_by_name(name):
    return session.query(Product).filter_by(name=name).first()

def insert_invoice(invoice_data):
    invoice = Invoice(
        customer_name=invoice_data['customer_name'],
        current_date=invoice_data['current_date'],
        grand_total=invoice_data['grand_total'],
        discount=invoice_data['discount'],
        receiving_amount=invoice_data['receiving_amount'],
        remaining_amount=invoice_data['remaining_amount'],
    )

    # Add related InvoiceItems
    for item in invoice_data['items']:
        invoice_item = InvoiceItem(
            product_name=item['product_name'],
            quantity=item['quantity'],
            sell_price=item['sell_price'],
            total_price=item['total_price'],
        )
        invoice.invoice_with_item.append(invoice_item)

        product = session.query(Product).filter_by(name=item['product_name']).first()
        if product:
            product.quantity -= item['quantity']
            session.commit()

    # Save the invoice to the database
    session.add(invoice)
    session.commit()
