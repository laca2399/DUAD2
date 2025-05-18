from flask import Blueprint, request, jsonify, Response
from jwt_manager import JWT_Manager
from products_manager import ProductDBManager
from user_manager import UserDBManager
from sqlalchemy import create_engine

products_bp = Blueprint('products', __name__)
db_manager = ProductDBManager()
user_manager = UserDBManager()
jwt_manager = JWT_Manager()

@products_bp.route('/products', methods=['POST'])
def create_product():
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    data = request.get_json()
    required_fields = ['name', 'sku', 'description', 'price', 'quantity', 'category_id', 'availability_id']
    if not all(field in data for field in required_fields):
        return Response(status=400)

    product = db_manager.insert_product(
        name=data['name'],
        sku=data['sku'],
        description=data['description'],
        price=data['price'],
        quantity=data['quantity'],
        category_id=data['category_id'],
        availability_id=data['availability_id']
    )

    return jsonify(
        id=product.id,
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=float(product.price),
        entry_date=product.entry_date.isoformat(),
        quantity=product.quantity,
        category_id=product.category_id,
        availability_id=product.availability_id
    )

@products_bp.route('/products', methods=['GET'])
def list_products():
    products = db_manager.get_all_products()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "sku": p.sku,
            "description": p.description,
            "price": float(p.price),
            "entry_date": p.entry_date.isoformat(),
            "quantity": p.quantity,
            "category_id": p.category_id,
            "availability_id": p.availability_id
        } for p in products
    ])

@products_bp.route('/products/<int:product_id>', methods=['GET'])
def get_product(product_id):
    product = db_manager.get_product_by_id(product_id)
    if not product:
        return Response(status=404)
    return jsonify(
        id=product.id,
        name=product.name,
        sku=product.sku,
        description=product.description,
        price=float(product.price),
        entry_date=product.entry_date.isoformat(),
        quantity=product.quantity,
        category_id=product.category_id,
        availability_id=product.availability_id
    )

@products_bp.route('/products/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    data = request.get_json()
    new_quantity = data.get('quantity')
    if new_quantity is None:
        return Response(status=400)

    product = db_manager.update_stock(product_id, new_quantity)
    if not product:
        return Response(status=404)

    return jsonify(message="Product updated")

@products_bp.route('/products/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    token = request.headers.get('Authorization')
    decoded = jwt_manager.decode(token.replace("Bearer ", "")) if token else None
    user = user_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user or user.role != "admin":
        return Response(status=403)

    deleted = db_manager.delete_product(product_id)
    if not deleted:
        return Response(status=404)
    return jsonify(message="Product deleted")

