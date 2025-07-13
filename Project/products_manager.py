from basemanager import BaseDBManager
from models import Product
from datetime import datetime, timezone


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
                entry_date=datetime.now(timezone.utc)
            )
            session.add(product)
            session.commit()
            session.refresh(product)
            product_data = {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "description": product.description,
                "price": float(product.price),
                "entry_date": product.entry_date.isoformat(),
                "quantity": product.quantity,
                "category_id": product.category_id,
                "availability_id": product.availability_id,
            }
            return product_data

    def get_all_products(self):
        with self.get_session() as session:
            products = session.query(Product).all()
            products_data = []
            for p in products:
                products_data.append({
                    "id": p.id,
                    "name": p.name,
                    "sku": p.sku,
                    "description": p.description,
                    "price": float(p.price),
                    "entry_date": p.entry_date.isoformat(),
                    "quantity": p.quantity,
                    "category_id": p.category_id,
                    "availability_id": p.availability_id,
                })
            return products_data

    def get_product_by_id(self, product_id):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if not product:
                return None
            product_data = {
                "id": product.id,
                "name": product.name,
                "sku": product.sku,
                "description": product.description,
                "price": float(product.price),
                "entry_date": product.entry_date.isoformat(),
                "quantity": product.quantity,
                "category_id": product.category_id,
                "availability_id": product.availability_id,
            }
            return product_data

    def update_stock(self, product_id, new_quantity):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                product.quantity = new_quantity
                session.commit()
                session.refresh(product)
                product_data = {
                    "id": product.id,
                    "name": product.name,
                    "sku": product.sku,
                    "description": product.description,
                    "price": float(product.price),
                    "entry_date": product.entry_date.isoformat(),
                    "quantity": product.quantity,
                    "category_id": product.category_id,
                    "availability_id": product.availability_id,
                }
                return product_data
            return None

    def delete_product(self, product_id):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            if product:
                session.delete(product)
                session.commit()
                return True
            return False
