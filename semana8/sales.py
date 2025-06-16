from flask import Blueprint, request, jsonify, Response
from jwt_manager import JWT_Manager
from productmanager import ProductDBManager
from salesmanager import SaleDBManager
from sqlalchemy import create_engine

sales_bp = Blueprint('sales', __name__)
product_manager = ProductDBManager()
sale_manager = SaleDBManager()
jwt_manager = JWT_Manager()

@sales_bp.route('/buy', methods=['POST'])
def buy_product():
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not decoded:
        return Response(status=403)
    user_id = decoded["sub"]

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or not quantity:
        return Response(status=400)

    product = product_manager.get_product_by_id(product_id)
    if not product or product.quantity < quantity:
        return Response(status=404)

    total = product.price * quantity
    invoice = sale_manager.insert_invoice(user_id, total)
    sale = sale_manager.insert_sale(invoice.id, product.id, quantity, product.price)
    product_manager.update_stock(product.id, product.quantity - quantity)

    return jsonify(invoice_id=invoice.id, sale_id=sale.id)

@sales_bp.route('/invoices', methods=['GET'])
def list_invoices():
    token = request.headers.get('Authorization')
    if not token or not token.startswith("Bearer "):
        return Response(status=401)
    decoded = jwt_manager.decode(token.replace("Bearer ", ""))
    if not decoded:
        return Response(status=401)

    user_id = decoded["sub"]
    invoices = sale_manager.get_invoices_by_user(user_id)

    return jsonify([
        {
            "invoice_id": inv.id,
            "total": float(inv.total),
            "created_at": inv.created_at.isoformat()
        } for inv in invoices
    ])
