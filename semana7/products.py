from flask import Blueprint, request, jsonify, Response
from datahandler import DB_Manager
from jwt_manager import JWT_Manager
from sqlalchemy import create_engine
from datetime import datetime

products_bp = Blueprint('products', __name__)

@products_bp.before_app_request
def setup_db_manager():
    engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
    global db_manager
    db_manager = DB_Manager(engine)

jwt_manager = JWT_Manager()

def is_admin(request):
    token = request.headers.get('Authorization')
    if token:
        decoded = jwt_manager.decode(token.replace("Bearer ", ""))
        user = db_manager.get_user_by_id(decoded["sub"])
        return user.role == "admin"
    return False


@products_bp.route('/', methods=["POST"])
def create_product():
    if not is_admin(request):
        return Response(status=403)
    
    data = request.get_json()
    name = data.get('name')
    price = data.get('price')
    quantity = data.get('quantity')

    if not name or not price or not quantity:
        return Response(status=400)

    new_product = db_manager.insert_product(name, price, quantity)  
    
    return jsonify(product=new_product)

@products_bp.route('/', methods=["GET"])
def list_products():
    products = db_manager.get_all_products()
    products_list = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "entry_date": p.entry_date.isoformat(),
            "quantity": p.quantity
        }
        for p in products
    ]
    return jsonify(products_list)



