from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base, User, Product, Invoice, Sale
from datetime import datetime

class DB_Manager:
    def __init__(self, engine):
        self.Session = sessionmaker(bind=engine)
        self.engine = engine

    def get_session(self):
        return self.Session()

    def insert_user(self, username, password, role="user"):
        session = self.get_session()
        new_user = User(username=username, password=password, role=role)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        session.close()
        return new_user

    def get_user(self, username, password):
        session = self.get_session()
        user = session.query(User).filter_by(username=username, password=password).first()
        session.close()
        return user
    
    def get_user_by_username(self, username):
        session = self.get_session()
        user = session.query(User).filter_by(username=username).first()
        session.close()
        return user

    
    def get_user_by_id(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        return user
    
    def get_user_role(self, user_id):
        session = self.get_session()
        user = session.query(User).filter_by(id=user_id).first()
        session.close()
        if user:
            return user.role
        return None

    def verify_password(self, user, password):
        return user.password == password


    def insert_product(self, name, price, quantity):
        session = self.get_session()
        new_product = Product(name=name, price=price, quantity=quantity)
        session.add(new_product)
        session.commit()
        session.refresh(new_product)
        session.close()
        return {"id": new_product.id, "name": new_product.name, "price": new_product.price, "entry_date": new_product.entry_date, "quantity": new_product.quantity}
    
    def get_all_products(self):
        session = self.Session()
        products = session.query(Product).all()
        return products
    
    def get_product_by_id(self, product_id):
        session = self.Session()
        product = session.query(Product).filter_by(id=product_id).first()
        return product


    
    def insert_invoice(self, user_id, total, created_at):
        session = self.get_session()
        new_invoice = Invoice(user_id=user_id, total=total, created_at=created_at)
        session.add(new_invoice)
        session.commit()
        session.refresh(new_invoice)
        session.close()
        return new_invoice

    def get_invoice(self, invoice_id):
        session = self.get_session()
        invoice = session.query(Invoice).filter_by(id=invoice_id).first()
        session.close()
        return invoice

    def insert_sale(self, invoice_id, product_id, quantity, price):
        session = self.get_session()
        new_sale = Sale(invoice_id=invoice_id, product_id=product_id, quantity=quantity, price=price)
        session.add(new_sale)
        session.commit()
        session.refresh(new_sale)
        session.close()
        return new_sale

    def get_sale(self, sale_id):
        session = self.get_session()
        sale = session.query(Sale).filter_by(id=sale_id).first()
        session.close()
        return sale
    
# Setup engine and session
engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")

# Create tables if they do not exist
Base.metadata.create_all(engine)

def create_default_admin():
    session = sessionmaker(bind=engine)()
    admin = session.query(User).filter_by(username='admin').first()
    if not admin: 
        db_manager = DB_Manager(engine)
        db_manager.insert_user("admin", "adminpassword", role="admin")
        print("Admin created.")
    session.close()

create_default_admin()