from flask import Blueprint, request, Response, jsonify
from datahandler import DB_Manager
from jwt_manager import JWT_Manager
from sqlalchemy import create_engine

users_bp = Blueprint('users', __name__)

@users_bp.before_app_request
def setup_db_manager():
    engine = create_engine("postgresql+psycopg2://postgres:Lacayo2020!@localhost:5432/postgres")
    global db_manager
    db_manager = DB_Manager(engine)

jwt_manager = JWT_Manager()

@users_bp.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    if data.get('username') is None or data.get('password') is None:
        return Response(status=400)
    else:
        result = db_manager.insert_user(data.get('username'), data.get('password'))
        user_id = result.id
        token = jwt_manager.encode(user_id)  
        return jsonify(token=token)


@users_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = db_manager.get_user_by_username(username)
    if user and db_manager.verify_password(user, password):
        role = db_manager.get_user_role(user.id)  
        token = jwt_manager.encode(user.id, role)  
        return jsonify({"token": token})
    else:
        return Response(status=401)



@users_bp.route('/me')
def me():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return Response(status=401)  # No token
        parts = token.split()
        if parts[0].lower() != "bearer" or len(parts) != 2:
            return Response(status=401)  # Invalid Authorization format
        clean_token = parts[1]
        decoded = jwt_manager.decode(clean_token)
        print(f"Decoded token: {decoded}")
        if decoded is None:
            return Response(status=403)  # Invalid token
        user_id = decoded['sub']
        user = db_manager.get_user_by_id(user_id)
        if user is None:
            return Response(status=404)  # User not found

        user_role = db_manager.get_user_role(user_id)
        if user_role == "admin":
            return jsonify(id=user.id, username=user.username, role=user_role)
        else:
            return jsonify(id=user.id, username=user.username)

    except Exception as e:
        return Response(status=500)  # Internal error
