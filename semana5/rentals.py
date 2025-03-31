from flask import Blueprint, request, jsonify
from database import PgManager  

rentals_bp = Blueprint('rentals', __name__)
db_manager = PgManager(db_name="lyfter_car_rental", user="postgres", password="Lacayo2020!", host="localhost")

@rentals_bp.route('/', methods=["POST"])
def create_rental():
    data = request.get_json()
    user_id = data.get("user_id")
    car_id = data.get("car_id")

    query_user = "SELECT status FROM lyfter_car_rental.users WHERE id = %s"
    user_result = db_manager.execute_query(query_user, user_id)
    
    if not user_result or user_result[0][0] != "active":
        return jsonify({"error": "User is not active"}), 400
    
    query_car = "SELECT status FROM lyfter_car_rental.cars WHERE id = %s"
    car_result = db_manager.execute_query(query_car, car_id)

    if not car_result or car_result[0][0] != "available":
        return jsonify({"error": "Car is not available"}), 400

    query_rental = """
        INSERT INTO lyfter_car_rental.rentals (user_id, car_id, rental_status)
        VALUES (%s, %s, %s) RETURNING rental_id
    """
    result = db_manager.execute_query(query_rental, user_id, car_id, "active")
    
    if result:
        rental_id = result[0][0]
        return jsonify({"message": "Rental created successfully", "rental_id": rental_id}), 201
    else:
        return jsonify({"error": "Error creating rental"}), 400

@rentals_bp.route('/<int:rental_id>/complete', methods=["PUT"])
def complete_rental(rental_id):

    query_rental = "SELECT rental_status, car_id FROM lyfter_car_rental.rentals WHERE rental_id = %s"
    rental_result = db_manager.execute_query(query_rental, rental_id)

    if not rental_result or rental_result[0][0] != "active":
        return jsonify({"error": "Rental not found or already completed"}), 404

    car_id = rental_result[0][1]
    
    query_update_rental = """
        UPDATE lyfter_car_rental.rentals
        SET rental_status = %s
        WHERE rental_id = %s
    """
    db_manager.execute_query(query_update_rental, "completed", rental_id)
    
    query_update_car = """
        UPDATE lyfter_car_rental.cars
        SET status = %s
        WHERE id = %s
    """
    db_manager.execute_query(query_update_car, "available", car_id)

    return jsonify({"message": "Rental completed and car is now available"}), 200

@rentals_bp.route("/rentals/<int:rental_id>/status", methods=["PUT"])
def change_rental_status(rental_id):
    data = request.get_json()
    new_status = data.get("status")

    if new_status not in ["active", "completed", "canceled"]:
        return jsonify({"error": "Invalid status. Use 'active', 'completed', or 'canceled'"}), 400

    query = "UPDATE lyfter_car_rental.rentals SET rental_status = %s WHERE rental_id = %s RETURNING rental_id"
    result = db_manager.execute_query(query, new_status, rental_id)

    if result:
        return jsonify({"message": f"Rental status updated to {new_status}"}), 200
    else:
        return jsonify({"error": "Rental not found"}), 404
    
@rentals_bp.route("/rentals", methods=["GET"])
def list_rentals():
    filters = []
    values = []

    user_id = request.args.get("user_id")
    car_id = request.args.get("car_id")
    rental_status = request.args.get("rental_status")  

    if user_id:
        filters.append("user_id = %s")
        values.append(user_id)
    if car_id:
        filters.append("car_id = %s")
        values.append(car_id)
    if rental_status:  
        filters.append("rental_status = %s")
        values.append(rental_status)

    base_query = "SELECT rental_id, user_id, car_id, rental_status FROM lyfter_car_rental.rentals"
    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    result = db_manager.execute_query(base_query, *values)

    if result:
        rentals = [
            {"rental_id": row[0], "user_id": row[1], "car_id": row[2], "rental_status": row[3]}
            for row in result
        ]
        return jsonify(rentals), 200
    else:
        return jsonify([]), 200
