from flask import Blueprint, request, jsonify, Response
from jwt_manager import JWT_Manager
from usermanager import UserDBManager
from sqlalchemy import create_engine

users_bp = Blueprint('users', __name__)
db_manager = UserDBManager()
jwt_manager = JWT_Manager()

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('username') or not data.get('password'):
        return Response(status=400)
    user = db_manager.insert_user(data['username'], data['password'])
    token = jwt_manager.encode(user.id)
    return jsonify(token=token)

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db_manager.get_user_by_username(data.get('username'))
    if user and db_manager.verify_password(user, data.get('password')):
        token = jwt_manager.encode(user.id, user.role)
        return jsonify(token=token)
    return Response(status=401)

@users_bp.route('/me', methods=['GET'])
def me():
    token = request.headers.get('Authorization')
    if not token or not token.lower().startswith("bearer "):
        return Response(status=401)
    decoded = jwt_manager.decode(token.split()[1])
    user = db_manager.get_user_by_id(decoded['sub']) if decoded else None
    if not user:
        return Response(status=404)
    return jsonify(id=user.id, username=user.username, role=user.role)