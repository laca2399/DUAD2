from basemanager import BaseDBManager
from models import Cart, CartItem, Invoice, Sale, Product
from datetime import datetime

class SaleDBManager(BaseDBManager):

    def create_cart(self, user_id):
        with self.get_session() as session:
            cart = Cart(user_id=user_id, created_at=datetime.utcnow(), status="active")
            session.add(cart)
            session.commit()
            return cart

    def add_product_to_cart(self, cart_id, product_id, quantity):
        with self.get_session() as session:
            product = session.query(Product).filter_by(id=product_id).first()
            cart = session.query(Cart).filter_by(id=cart_id, status="active").first()
            if not product or not cart or product.quantity < quantity:
                return False
            item = CartItem(cart_id=cart_id, product_id=product_id, quantity=quantity)
            session.add(item)
            session.commit()
            return True

    def remove_product_from_cart(self, cart_id, product_id):
        with self.get_session() as session:
            item = session.query(CartItem).filter_by(cart_id=cart_id, product_id=product_id).first()
            if item:
                session.delete(item)
                session.commit()
                return True
            return False

    def checkout_cart(self, cart_id):
        with self.get_session() as session:
            cart = session.query(Cart).filter_by(id=cart_id, status="active").first()
            if not cart or not cart.items:
                return None

            total = 0
            for item in cart.items:
                product = session.query(Product).filter_by(id=item.product_id).first()
                if not product or product.quantity < item.quantity:
                    return None
                total += product.price * item.quantity
                product.quantity -= item.quantity

            invoice = Invoice(user_id=cart.user_id, total=total, created_at=datetime.utcnow())
            session.add(invoice)
            session.commit()

            for item in cart.items:
                product = session.query(Product).filter_by(id=item.product_id).first()
                sale = Sale(
                    invoice_id=invoice.id,
                    product_id=item.product_id,
                    quantity=item.quantity,
                    price=session.query(Product).filter_by(id=item.product_id).first().price
                )
                session.add(sale)

            cart.status = "completed"
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
