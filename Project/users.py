from flask import Blueprint, request, jsonify, Response
from jwt_manager import JWT_Manager
from user_manager import UserDBManager
from sqlalchemy import create_engine

users_bp = Blueprint('users', __name__)
engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
db_manager = UserDBManager(engine)
jwt_manager = JWT_Manager()

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if not data.get('email') or not data.get('password') or not data.get('name'):
        return Response(status=400)
    user = db_manager.insert_user(data['email'], data['password'], data['name'])
    token = jwt_manager.encode(user.id)
    return jsonify(token=token)

@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = db_manager.get_user_by_email(data.get('email'))
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
    return jsonify(id=user.id, email=user.email, role=user.role)