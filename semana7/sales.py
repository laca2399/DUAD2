from flask import Blueprint, request, jsonify, Response
from datahandler import DB_Manager
from jwt_manager import JWT_Manager
from sqlalchemy import create_engine

sales_bp = Blueprint('sales', __name__)
print("sales.py imported")

@sales_bp.before_app_request
def setup_db_manager():
    engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
    global db_manager
    db_manager = DB_Manager(engine)

jwt_manager = JWT_Manager()

@sales_bp.route('/buy', methods=['POST'])
def buy_product():
    token = request.headers.get('Authorization')
    if not token:
        return Response(status=401)  
    decoded = jwt_manager.decode(token.replace("Bearer ", ""))
    if decoded is None:
        return Response(status=403) 
    user_id = decoded["sub"]

    data = request.get_json()
    product_id = data.get("product_id")
    quantity = data.get("quantity")

    if not product_id or not quantity:
        return Response(status=400)  

    product = db_manager.get_product_by_id(product_id)

    if not product or product.quantity < quantity:
        return Response(status=404)  

    #Calculate total
    total = product.price * quantity

    #Create invoice
    invoice = db_manager.insert_invoice(user_id, total)

    #Close sale
    sale = db_manager.insert_sale(invoice.id, product.id, quantity, product.price)

    #Update stock
    db_manager.insert_product(product_id, product.price, product.quantity - quantity)

    return jsonify(invoice_id=invoice.id, sale_id=sale.id)


