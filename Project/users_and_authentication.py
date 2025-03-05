from flask import Flask, request, jsonify
import secrets

users_list = [
    {"email": "andy231999@gmail.com", "password": "securep123p", "role": "admin"}
]

valid_tokens = []

@app.route('/auth/register', methods=['POST'])
def register_user():
    try:
        if "email" not in request.json:
            raise ValueError("email missing from the body")

        if "password" not in request.json:
            raise ValueError("password missing from the body")

        users_list.append(
            {
                "email": request.json["email"],
                "password": request.json["password"],
                "role": "client"

            }
        )
        return jsonify(message="User registered successfully"), 201
    
    except ValueError as ex:
        return jsonify(message=str(ex)), 400



@app.route('/auth/login', methods=['POST'])
def login_user():
    try:
        if "email" not in request.json:
            raise ValueError("email missing from the body")

        if "password" not in request.json:
            raise ValueError("password missing from the body")

        user = next((u for u in users_list if u["email"] == request.json["email"]), None)

        if not user:
            return jsonify(message="User not found"), 404

        if user["password"] != request.json["password"]:
            return jsonify(message="Invalid password"), 401
        
        token = secrets.token_hex(16)
        valid_tokens.append(token)

        return jsonify(message="Login successful", token=token, role=user["role"])

    except ValueError as ex:
        return jsonify(message=str(ex)), 400


@app.route('/view-token')
def view_token():
    token = request.headers.get('token', '')
    if token not in valid_tokens:
        return jsonify(message="Invalid token"), 401
    return jsonify(message="Token valid", token=token)



def check_role(required_role):
    token = request.headers.get('token', '')
    if token not in valid_tokens:
        return jsonify(message="Invalid token"), 401
    
    user = next((u for u in users_list if u["email"] == request.json["email"]), None) 

    if not user or user["role"]!= required_role:
        return jsonify(message="Access denied. You don't have the required role."), 403
    
    return None

def check_admin_role():
    token = request.headers.get('token', '')
    if token not in valid_tokens:
        return jsonify(message="Invalid token"), 401
    
    user_role = request.headers.get('role', 'client')  # Esto puede variar dependiendo de cómo manejes la autenticación
    if user_role != "admin":
        return jsonify(message="You do not have permission to perform this action."), 403
    
    return None
