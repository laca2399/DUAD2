from flask import Blueprint, request, jsonify, Response, current_app
from jwt_manager import JWT_Manager
from controllers.products_manager import ProductDBManager
from controllers.user_manager import UserDBManager
import json


products_bp = Blueprint('products', __name__)
db_manager = ProductDBManager()
user_manager = UserDBManager()
jwt_manager = JWT_Manager()

@products_bp.route('/products', methods=['POST'])
def create_product():
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user["role"] != "admin":
        return Response(status=403)

    data = request.get_json()
    required_fields = ['name', 'sku', 'description', 'price', 'quantity', 'category_id', 'availability_id']
    if not all(field in data for field in required_fields):
        return Response(status=400)

    product_data = db_manager.insert_product(
        name=data['name'],
        sku=data['sku'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity'],
        category_id=data['category_id'],
        availability_id=data['availability_id']
    )

    current_app.cache.delete_data("product_list")

    return jsonify(product_data)

@products_bp.route('/products', methods=['GET'])
def list_products():

    product_list_key = "product_list"
    cached_products = current_app.cache.get_data(product_list_key)
    if cached_products:
        return jsonify(json.loads(cached_products))

    products_data = db_manager.get_all_products()
    current_app.cache.store_data(product_list_key, json.dumps(products_data), time_to_live=300)
    return jsonify(products_data)

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):

    product_key = f"product:{product_id}"
    cached_product = current_app.cache.get_data(product_key)
    if cached_product:
        return jsonify(json.loads(cached_product))

    product_data = db_manager.get_product_by_id(product_id)
    if not product_data:
        return Response(status=404)

    current_app.cache.store_data(product_key, json.dumps(product_data), time_to_live=300)
    return jsonify(product_data)

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user["role"] != "admin":
        return Response(status=403)

    data = request.get_json()
    new_quantity = data.get('quantity')
    if new_quantity is None:
        return Response(status=400)

    updated_product_data = db_manager.update_stock(product_id, new_quantity)
    if not updated_product_data:
        return Response(status=404)

    product_key = f"product:{product_id}"
    current_app.cache.delete_data(product_key)

    product_list_key = "product_list"
    current_app.cache.delete_data(product_list_key)

    return jsonify(message="Product updated")

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user["role"] != "admin":
        return Response(status=403)

    deleted = db_manager.delete_product(product_id)
    if not deleted:
        return Response(status=404)
    
    product_key = f"product:{product_id}"
    current_app.cache.delete_data(product_key)

    product_list_key = "product_list"
    current_app.cache.delete_data(product_list_key)

    return jsonify(message="Product deleted")

