from sqlalchemy import Column, Integer, String, Numeric, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base
from datetime import datetime

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(155), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    name = Column(String(100), nullable=False)
    role = Column(String(50), nullable=False, default="client")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)

    def __repr__(self):
        return f"<User(id={self.id}, email={self.email}, password={self.password}, name={self.name}, role={self.role}, created_at={self.created_at}, is_active={self.is_active})>"
    
class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), nullable=False)
    
    def __repr__(self):
        return f"<User(id={self.id}, name={self.name})>"

class User_Role(Base):
    __tablename__ = 'user_roles'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    role_id = Column(Integer, ForeignKey('roles.id'), nullable=False)


    def __repr__(self):
        return f"<User(id={self.id}, user_id={self.user_id}, role_id={self.role_id})>"
    
class Availability(Base):
    __tablename__ = 'availability'

    id = Column(Integer, primary_key=True)
    status = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Availability(id={self.id}, status={self.status})>"

class Product_Category(Base):
    __tablename__ = 'product_categories'

    id = Column(Integer, primary_key=True)
    name = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Product_Category(id={self.id}, status={self.name})>"
    
class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    sku = Column(Integer, unique=True, nullable=False)
    availability_id = Column(Integer, ForeignKey('availability.id'), nullable=False)
    category_id = Column(Integer, ForeignKey('product_categories.id'), nullable=False)
    name = Column(String(155), unique=True, nullable=False)
    description = Column(String(255), nullable=False)
    price = Column(Numeric(10, 2), nullable=False)
    quantity = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Product(id={self.id}, sku={self.sku}, availability_id={self.availability_id}, category_id={self.category_id}, name={self.name}, description={self.description}, price={self.price}, quantity={self.quantity}, created_at={self.created_at}, updated_at={self.updated_at})>"

class Invoice_Status(Base):
    __tablename__ = 'invoice_status'

    id = Column(Integer, primary_key=True)
    status = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Invoice_Status(id={self.id}, status={self.status})>"
    
class Cart_Status(Base):
    __tablename__ = 'cart_status'

    id = Column(Integer, primary_key=True)
    status = Column(String(100), unique=True, nullable=False)

    def __repr__(self):
        return f"<Cart_Status(id={self.id}, status={self.status})>"
    

class Cart(Base):
    __tablename__ = 'carts'

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    cart_status_id = Column(Integer, ForeignKey('cart_status.id'), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, nullable=False)

    def __repr__(self):
        return f"<Cart(id={self.id}, user_id={self.user_id}, cart_status_id={self.cart_status_id}, created_at={self.created_at}, updated_at={self.updated_at})>"
    

class Invoice(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    user_id = Column(Integer, ForeignKey('users.id'), nullable=False)
    invoice_status_id = Column(Integer, ForeignKey('invoice_status.id'), nullable=False)
    billing_address = Column(String(255), nullable=False)
    total_amount = Column(Numeric(10, 2), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    

    def __repr__(self):
        return f"<Invoice(id={self.id}, cart_id={self.cart_id}, user_id={self.user_id}, invoice_status_id={self.invoice_status_id}, billing_address={self.billing_address}, total_amount={self.total_amount}, created_at={self.created_at})>"
    

class Cart_Products(Base):
    __tablename__ = 'cart_products'

    id = Column(Integer, primary_key=True)
    cart_id = Column(Integer, ForeignKey('carts.id'), nullable=False)
    product_id = Column(Integer, ForeignKey('products.id'), nullable=False)
    quantity = Column(Integer, nullable=False)


    def __repr__(self):
        return f"<Cart_Status(id={self.id}, cart_id={self.cart_id}, product_id={self.product_id}, quantity={self.quantity})>"
    