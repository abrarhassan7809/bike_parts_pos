# db_operations.py
import random
from datetime import datetime
from sqlalchemy import func
from db_config.models import Product, Invoice, InvoiceItem, Supplier, Customer
from db_config.db import SessionLocal
session = SessionLocal()

def insert_product(name, company, rank_number, pur_price, sel_price, quantity, current_date):
    product = Product(name=name, company=company, rank_number=rank_number, pur_price=round(pur_price, 2),
                      sel_price=round(sel_price, 2), quantity=quantity, current_date=current_date)
    session.add(product)
    session.commit()

def update_product(product_id, name=None, company=None, rank_number=None, pur_price=None,sel_price=None, quantity=None):
    product = session.query(Product).filter_by(id=product_id).first()
    if name:
        product.name = name
    if company:
        product.company = company
    if rank_number:
        product.rank_number = rank_number
    if pur_price:
        product.pur_price = round(pur_price, 2)
    if sel_price:
        product.sel_price = round(sel_price, 2)
    if quantity:
        product.quantity = quantity
    session.commit()

def delete_product(product_id):
    product = session.query(Product).filter_by(id=product_id).first()
    session.delete(product)
    session.commit()


def insert_products_from_file(products_data):
    errors = []
    success_count = 0
    for product_data in products_data:
        product_data['pur_price'] = float(product_data['pur_price'])
        product_data['sel_price'] = float(product_data['sel_price'])
        product_data['quantity'] = int(product_data['quantity'])
        product_data['current_date'] = datetime.now().strftime('%Y-%m-%d')

        result = insert_or_update_product(product_data)
        if "Error" in result:
            errors.append(result)
        else:
            success_count += 1

    session.commit()
    error_message = f"\nErrors:\n{', '.join(errors)}" if errors else ""
    return f"Imported {success_count} products successfully.{error_message}"

def delete_customer(customer_id):
    customer = session.query(Customer).filter_by(id=customer_id).first()
    session.delete(customer)
    session.commit()

def delete_supplier(supplier_id):
    supplier = session.query(Supplier).filter_by(id=supplier_id).first()
    session.delete(supplier)
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

def get_today_invoices():
    today = datetime.now().date()
    today_invoices = session.query(Invoice).filter(func.date(Invoice.current_date) == today).all()
    return today_invoices

def insert_supplier(name, company, phone_num, email, address):
    supplier = Supplier(name=name, company=company, phon_num=phone_num, email=email, address=address)
    session.add(supplier)
    session.commit()

def insert_customer(name, company, phone_num, email, city, address):
    customer = Customer(name=name, company=company, phone_num=phone_num, email=email, city=city, address=address)
    session.add(customer)
    session.commit()

def get_all_suppliers():
    suppliers = session.query(Supplier).all()
    return suppliers

def get_all_customers():
    customers = session.query(Customer).all()
    return customers

def get_product_by_id(p_id):
    products = session.query(Product).filter_by(id=p_id).first()
    return products

def get_product_by_name(name):
    return session.query(Product).filter_by(name=name).first()

def insert_or_update_product(data):
    try:
        existing_product = session.query(Product).filter_by(name=data['name'], company=data['company']).first()

        if existing_product:
            existing_product.quantity += data['quantity']
            existing_product.pur_price = round(data['pur_price'], 2)
            existing_product.sel_price = round(data['sel_price'], 2)
            session.commit()
            return "Product updated successfully"
        else:
            insert_product(**data)
            return "Product added successfully"
    except Exception as e:
        session.rollback()
        return f"Error: {str(e)}"

def generate_unique_invoice_code():
    while True:
        code = f"{random.randint(1000, 9999)}"
        if not check_invoice_code_exists(code):
            return code

def check_invoice_code_exists(code):
    code_exist = session.query(Invoice).filter_by(invoice_code=code).first()
    if code_exist:
        return code_exist
    else:
        return None

def insert_invoice(invoice_data):
    invoice_code = generate_unique_invoice_code()
    invoice = Invoice(
        customer_name=invoice_data['customer_name'],
        current_date=invoice_data['current_date'],
        grand_total=invoice_data['grand_total'],
        discount=invoice_data['discount'],
        receiving_amount=invoice_data['receiving_amount'],
        remaining_amount=invoice_data['remaining_amount'],
        invoice_code=invoice_code,
    )

    for item in invoice_data['items']:
        invoice_item = InvoiceItem(
            product_name=item['product_name'],
            company=item['company'],
            quantity=item['quantity'],
            sell_price=item['sell_price'],
            total_price=item['total_price'],
        )
        invoice.invoice_with_item.append(invoice_item)

        product = session.query(Product).filter_by(name=item['product_name']).first()
        if product:
            product.quantity -= item['quantity']
            if product.quantity < 0:
                product.quantity = 0

    try:
        session.add(invoice)
        session.commit()
    except Exception as e:
        session.rollback()
    finally:
        session.close()

def get_daily_sales():
    today = datetime.now().date()
    sales = session.query(func.sum(Invoice.grand_total)).filter(func.date(Invoice.current_date) == today).scalar()
    return sales if sales else 0

def get_daily_profit():
    today = datetime.now().date()
    profit = 0

    invoices = session.query(Invoice).filter(func.date(Invoice.current_date) == today).all()
    for invoice in invoices:
        invoice_profit = 0
        for item in invoice.invoice_with_item:
            product = session.query(Product).filter_by(name=item.product_name).first()
            if product:
                invoice_profit += (item.sell_price - product.pur_price) * item.quantity
        profit += invoice_profit - invoice.discount

    return profit

def get_monthly_sales():
    start_of_month = datetime.now().replace(day=1).date()
    sales = session.query(func.sum(Invoice.grand_total)).filter(func.date(Invoice.current_date) >= start_of_month).scalar()
    return sales if sales else 0

def get_monthly_profit():
    start_of_month = datetime.now().replace(day=1).date()
    profit = 0

    invoices = session.query(Invoice).filter(func.date(Invoice.current_date) >= start_of_month).all()
    for invoice in invoices:
        invoice_profit = 0
        for item in invoice.invoice_with_item:
            product = session.query(Product).filter_by(name=item.product_name).first()
            if product:
                invoice_profit += (item.sell_price - product.pur_price) * item.quantity
        profit += invoice_profit - invoice.discount

    return profit

def get_total_counts():
    total_products = session.query(func.count(Product.id)).scalar()
    total_invoices = session.query(func.count(Invoice.id)).scalar()
    total_customers = session.query(func.count(Customer.id)).scalar()
    return {
        'total_products': total_products,
        'total_customers': total_customers,
        'total_invoices': total_invoices,
    }

