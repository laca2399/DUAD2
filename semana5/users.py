from flask import Blueprint, request, jsonify
from database import PgManager  

users_bp = Blueprint('users', __name__)
db_manager = PgManager(db_name="lyfter_car_rental", user="postgres", password="Lacayo2020!", host="localhost")


@users_bp.route('/', methods=["POST"])
def create_user():
    data = request.get_json()
    name = data.get("name")
    email = data.get("email")
    username = data.get("username")
    password = data.get("password")
    birthdate = data.get("birthdate")

    query = """
        INSERT INTO lyfter_car_rental.users (name, email, username, password, birthdate)
        VALUES (%s, %s, %s, %s, %s) RETURNING id
    """
    result = db_manager.execute_query(query, name, email, username, password, birthdate)

    if result:
        return jsonify({"message": "User created successfully", "user_id": result[0][0]}), 201
    else:
        return jsonify({"error": "Error when creating user"}), 500


@users_bp.route('/<int:user_id>/status', methods=["PUT"])
def change_user_status(user_id):
    data = request.get_json()
    new_status = data.get("status")  

    if new_status not in ["active", "inactive", "defaulter"]:
        return jsonify({"error": "Invalid status. Use 'active', 'inactive' o 'defaulter'"}), 400

    query = "UPDATE lyfter_car_rental.users SET status = %s WHERE id = %s RETURNING id"
    result = db_manager.execute_query(query, new_status, user_id)

    if result:
        return jsonify({"message": f"User status updated to {new_status}"}), 200
    else:
        return jsonify({"error": "User not found"}), 404

@users_bp.route("/users/<int:user_id>/defaulter", methods=["PUT"])
def mark_user_defaulter(user_id):
    return change_user_status(user_id, "defaulter")

@users_bp.route("/users", methods=["GET"])
def list_users():
    filters = []
    values = []

    name = request.args.get("name")
    email = request.args.get("email")
    username = request.args.get("username")  
    status = request.args.get("status")

    if name:
        filters.append("name ILIKE %s")
        values.append(f"%{name}%")
    if email:
        filters.append("email ILIKE %s")
        values.append(f"%{email}%")
    if username:  
        filters.append("username ILIKE %s")
        values.append(f"%{username}%")
    if status:
        filters.append("status = %s")
        values.append(status)

    base_query = "SELECT id, name, email, username, status FROM lyfter_car_rental.users"
    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    result = db_manager.execute_query(base_query, *values)

    if result:
        users = [
            {"id": row[0], "name": row[1], "email": row[2], "username": row[3], "status": row[4]}
            for row in result
        ]
        return jsonify(users), 200
    else:
        return jsonify([]), 200
