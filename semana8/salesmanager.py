from basemanager import BaseDBManager
from models import Sale, Invoice
from datetime import datetime

class SaleDBManager(BaseDBManager):
    def insert_invoice(self, user_id, total):
        with self.get_session() as session:
            invoice = Invoice(user_id=user_id, total=total, created_at=datetime.utcnow())
            session.add(invoice)
            session.commit()
            return invoice

    def insert_sale(self, invoice_id, product_id, quantity, price):
        with self.get_session() as session:
            sale = Sale(invoice_id=invoice_id, product_id=product_id, quantity=quantity, price=price)
            session.add(sale)
            session.commit()
            return sale

    def get_invoices_by_user(self, user_id):
        with self.get_session() as session:
            return session.query(Invoice).filter_by(user_id=user_id).all()