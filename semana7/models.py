from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    username = Column(String(100), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False, default="user")


    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, password={self.password}, role={self.role})>"
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    entry_date = Column(DateTime, default=datetime.utcnow, nullable=False)
    quantity = Column(Integer, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, name={self.name}, price={self.price}, entry_date={self.entry_date}, quantity={self.quantity})>"
    
class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    total = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Invoice(id={self.id}, user_id={self.user_id}, total={self.total}, created_at={self.created_at})>"
    
class Sale(Base):
    __tablename__= 'sales'

    id = Column(Integer, primary_key=True)
    invoice_id = Column(Integer, ForeignKey('invoices.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)
    price = Column(Numeric(10, 2), nullable=False)

    def __repr__(self):
        return f"<Sale(id={self.id}, invoice_id={self.invoice_id}, product_id={self.product_id}, quantity={self.quantity}, price={self.price})>"
    