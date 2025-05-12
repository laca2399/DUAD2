from basemanager import BaseDBManager
from models import Product
from datetime import datetime

class ProductDBManager(BaseDBManager):

    def insert_product(self, name, sku, description, price, quantity, category_id, availability_id):
        with self.get_session() as session:
            product = Product(
                name=name,
                sku=sku,
                description=description,
                price=price,
                quantity=quantity,
                category_id=category_id,
                availability_id=availability_id,
                entry_date=datetime.utcnow()
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            return product

    def get_all_products(self):
        with self.get_session() as session:
            return session.query(Product).all()

    def get_product_by_id(self, product_id):
        with self.get_session() as session:
            return session.query(Product).filter_by(id=product_id).first()

    def update_stock(self, product_id, new_quantity):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                product.quantity = new_quantity
                session.commit()
                session.refresh(product)
            return product

    def delete_product(self, product_id):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                session.delete(product)
                session.commit()
                return True
            return False
