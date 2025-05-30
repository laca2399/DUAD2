from flask import Blueprint, request, jsonify, Response, current_app
from jwt_manager import JWT_Manager
from productmanager import ProductDBManager
from usermanager import UserDBManager
from sqlalchemy import create_engine
import json

products_bp = Blueprint('products', __name__)
db_manager = ProductDBManager()
user_manager = UserDBManager()
jwt_manager = JWT_Manager()

@products_bp.route('/', methods=['POST'])
def create_product():
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    data = request.get_json()
    if not all([data.get('name'), data.get('price'), data.get('quantity')]):
        return Response(status=400)

    product = db_manager.insert_product(data['name'], data['price'], data['quantity'])


    return jsonify(id=product.id, name=product.name, price=float(product.price), entry_date=product.entry_date.isoformat(), quantity=product.quantity)

@products_bp.route('/', methods=['GET'])
def list_products():
    product_list_key = "product_list"
    cached_products = current_app.cache.get_data(product_list_key)
    if cached_products:
        return jsonify(json.loads(cached_products))

    products = db_manager.get_all_products()
    product_data = [
        {
            "id": p.id,
            "name": p.name,
            "price": float(p.price),
            "entry_date": p.entry_date.isoformat(),
            "quantity": p.quantity
        } for p in products
    ]

    current_app.cache.store_data(product_list_key, json.dumps(product_data), time_to_live=300)
    return jsonify(product_data)


@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product_key = f"product:{product_id}"
    # Try to obtain product from cache
    cached_product = current_app.cache.get_data(product_key)
    if cached_product:
        return jsonify(json.loads(cached_product))
    
    #If not in cache, then check db
    product = db_manager.get_product_by_id(product_id)
    if not product:
        return Response(status=404)
    
    product_data = {
        "id": product.id,
        "name": product.name,
        "price": float(product.price),
        "entry_date": product.entry_date.isoformat(),
        "quantity": product.quantity
    }
    current_app.cache.store_data(product_key, json.dumps(product_data), time_to_live=300) #Save for 300 seconds
    return jsonify(product_data)

@products_bp.route('/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    data=request.get_json()
    new_quantity = data.get('quantity')
    if new_quantity is None:
        return Response(status=400)
    
    product = db_manager.update_stock(product_id, new_quantity)
    if not product:
        return Response(status=404)
    
    product_key = f"product:{product_id}"
    current_app.cache.delete_data(product_key)

    product_list_key = "product_list"
    current_app.cache.delete_data(product_list_key)

    return jsonify(message="Product updated")

@products_bp.route('/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    deleted = db_manager.delete_product(product_id)
    if not deleted:
        return Response(status=404)
    
    product_key = f"product:{product_id}"
    current_app.cache.delete_data(product_key)

    product_list_key = "product_list"
    current_app.cache.delete_data(product_list_key)

    return jsonify(message="Product deleted")