from basemanager import BaseDBManager
from models import Cart, Cart_Products, Invoice, Sale, Product, Cart_Status
from datetime import datetime, timezone
from sqlalchemy.orm.exc import NoResultFound
class SaleDBManager(BaseDBManager):

    def create_cart(self, user_id):
        with self.get_session() as session:
            active_status = session.query(Cart_Status).filter_by(status="active").first()
            if not active_status:
                raise Exception("Active cart status not found in database.")
            cart = Cart(user_id=user_id, cart_status_id=active_status.id, created_at=datetime.now(timezone.utc), updated_at=datetime.now(timezone.utc))
            session.add(cart)
            session.commit()
            session.refresh(cart)
            return cart

    def add_product_to_cart(self, cart_id, product_id, quantity):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()

            active_status = session.query(Cart_Status).filter_by(status="active").first()
            if not active_status:
                return False
            
            cart = session.query(Cart).filter_by(id=cart_id, cart_status_id=active_status.id).first()
            if not product or not cart or product.quantity < quantity:
                return False
            item = Cart_Products(cart_id=cart_id, product_id=product_id, quantity=quantity)
            session.add(item)
            session.commit()
            return True

    def remove_product_from_cart(self, cart_id, product_id):
        with self.get_session() as session:
            item = session.query(Cart_Products).filter_by(cart_id=cart_id, product_id=product_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

    def checkout_cart(self, cart_id):
        with self.get_session() as session:
            active_status = session.query(Cart_Status).filter_by(status="active").first()
            if not active_status:
                return None
            
            cart = session.query(Cart).filter_by(id=cart_id, cart_status_id=active_status.id).first()
            if not cart or not hasattr(cart, 'items') or len(cart.items) == 0:
                return None

            total = 0
            for item in cart.items:
                product = session.query(Product).filter_by(id=item.product_id).first()
                if not product or product.quantity < item.quantity:
                    return None
                total += product.price * item.quantity
                product.quantity -= item.quantity

            invoice = Invoice(user_id=cart.user_id, total=total, created_at=datetime.now(timezone.utc))
            session.add(invoice)
            session.commit()

            for item in cart.items:
                product_price = session.query(Product).filter_by(id=item.product_id).first().price
                sale = Sale(
                    invoice_id=invoice.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=product_price
                )
                session.add(sale)
            
            completed_status = session.query(Cart_Status).filter_by(status="completed").first()
            if not completed_status:
                raise Exception("Completed cart status not found in database.")
            cart.cart_status_id = completed_status.id

            session.commit()
            return invoice

    def get_invoice(self, invoice_id):
        with self.get_session() as session:
            return session.query(Invoice).filter_by(id=invoice_id).first()

    def return_invoice(self, invoice_id):
        with self.get_session() as session:
            invoice = session.query(Invoice).filter_by(id=invoice_id).first()
            if not invoice:
                return False
            sales = session.query(Sale).filter_by(invoice_id=invoice_id).all()
            for sale in sales:
                product = session.query(Product).filter_by(id=sale.product_id).first()
                if product:
                    product.quantity += sale.quantity
            session.commit()
            return True
