from flask import Blueprint, request, jsonify, Response, current_app
from jwt_manager import JWT_Manager
from products_manager import ProductDBManager
from sales_manager import SaleDBManager
from user_manager import UserDBManager
import json

sales_bp = Blueprint('sales', __name__)

product_manager = ProductDBManager()
sale_manager = SaleDBManager()
user_manager = UserDBManager()
jwt_manager = JWT_Manager()

@sales_bp.route("/carts", methods=["POST"])
def create_cart():
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)

    cart = sale_manager.create_cart(user["sub"])
    return jsonify({"message": "Cart created", "cart_id": cart.id}), 201

@sales_bp.route("/carts/<int:cart_id>/add", methods=["POST"])
def add_to_cart(cart_id):
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity", 1)

    result = sale_manager.add_product_to_cart(cart_id, product_id, quantity)
    if not result:
        return jsonify({"message": "Product not found or insufficient stock"}), 400

    return jsonify({"message": "Product added to cart"}), 200

@sales_bp.route("/carts/<int:cart_id>/remove", methods=["POST"])
def remove_from_cart(cart_id):
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)

    product_id = request.get_json().get("product_id")
    sale_manager.remove_product_from_cart(cart_id, product_id)
    return jsonify({"message": "Product removed from cart"}), 200

@sales_bp.route("/carts/<int:cart_id>/checkout", methods=["POST"])
def checkout(cart_id):
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)

    result = sale_manager.checkout_cart(cart_id)
    if not result:
        return jsonify({"message": "Checkout failed. Check stock or cart status."}), 400

    return jsonify({"message": "Checkout successful", "invoice_id": result.id}), 200

@sales_bp.route("/invoices/<int:invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)
    
    invoice_key = f"invoice:{invoice_id}"
    cached_invoice = current_app.cache.get_data(invoice_key)
    if cached_invoice:
        return jsonify(json.loads(cached_invoice))

    invoice = sale_manager.get_invoice(invoice_id)
    if not invoice:
        return jsonify({"message": "Invoice not found"}), 404

    invoice_data = {
        "invoice_id": invoice.id,
        "total": float(invoice.total),
        "created_at": invoice.created_at.isoformat()
    }

    current_app.cache.store_data(invoice_key, json.dumps(invoice_data), time_to_live=300)

    return jsonify(invoice_data)

@sales_bp.route("/invoices/<int:invoice_id>/return", methods=["POST"])
def return_invoice(invoice_id):
    token = request.headers.get('Authorization')
    user = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    if not user:
        return Response(status=403)

    success = sale_manager.return_invoice(invoice_id)
    if not success:
        return jsonify({"message": "Return failed"}), 400
    
    invoice_key = f"invoice:{invoice_id}"
    current_app.cache.delete_data(invoice_key)

    return jsonify({"message": "Return processed, stock updated"}), 200