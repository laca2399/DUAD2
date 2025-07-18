from flask import Blueprint, request, jsonify, Response, current_app
from jwt_manager import JWT_Manager
from controllers.user_manager import UserDBManager
import json 

users_bp = Blueprint('users', __name__)
db_manager = UserDBManager()
jwt_manager = JWT_Manager()

@users_bp.route('/auth/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return Response(status=400)
    user = db_manager.insert_user(data['email'], data['password'], data['name'])
    token = jwt_manager.encode(user["id"])
    return jsonify(token=token)

@users_bp.route('/auth/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db_manager.get_user_by_email(data.get('email'))
    if user and db_manager.verify_password(user, data.get('password')):
        token = jwt_manager.encode(user["id"], user["role"])
        return jsonify(token=token)
    return Response(status=401)

@users_bp.route('/me', methods=['GET'])
def me():
    token = request.headers.get('Authorization')
    if not token or not token.lower().startswith("bearer "):
        return Response(status=401)
    decoded = jwt_manager.decode(token.split()[1])

    if not decoded:
        return Response(status=401)
    
    user_id = decoded['sub']
    cache_key = f"user:{user_id}"

    cached_user = current_app.cache.get_data(cache_key)
    if cached_user:
        return jsonify(json.loads(cached_user))
    
    user = db_manager.get_user_by_id(user_id)
    if not user:
        return Response(status=404)
    
    user_data = {
        "id": user['id'],
        "email": user['email'],
        "role": user['role']
    }

    current_app.cache.store_data(cache_key, json.dumps(user_data), time_to_live=300)

    return jsonify(user_data)