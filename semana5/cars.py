from flask import Blueprint, request, jsonify
from database import PgManager  

cars_bp = Blueprint('cars', __name__)
db_manager = PgManager(db_name="lyfter_car_rental", user="postgres", password="Lacayo2020!", host="localhost")

@cars_bp.route("/cars", methods=["POST"])
def create_car():
    data = request.get_json()
    brand = data.get("brand")
    model = data.get("model")
    year_of_manufacture = data.get("year_of_manufacture")

    query = """
    INSERT INTO lyfter_car_rental.cars (brand, model, year_of_manufacture)
    VALUES (%s, %s, %s) RETURNING id
    """

    result = db_manager.execute_query(query, brand, model, year_of_manufacture)

    if result:
        return jsonify({"message": "Car created successfully", "car_id": result[0][0]}), 201
    else:
        return jsonify({"error": "Error when creating car"}), 500

@cars_bp.route("/cars/<int:car_id>/status", methods=["PUT"])
def change_car_status(car_id):
    data = request.get_json()
    new_status = data.get("status")  

    if new_status not in ["available", "unavailable", "maintenance"]:
        return jsonify({"error": "Invalid status. Use 'available', 'unavailable', or 'maintenance'"}), 400

    query = "UPDATE lyfter_car_rental.cars SET status = %s WHERE id = %s RETURNING id"
    result = db_manager.execute_query(query, new_status, car_id)

    if result:
        return jsonify({"message": f"Car status updated to {new_status}"}), 200
    else:
        return jsonify({"error": "Car not found"}), 404
    
@cars_bp.route("/cars", methods=["GET"])
def list_cars():
    filters = []
    values = []

    brand = request.args.get("brand")
    model = request.args.get("model")  
    year_of_manufacture = request.args.get("year_of_manufacture")
    status = request.args.get("status")

    if brand:
        filters.append("brand ILIKE %s")
        values.append(f"%{brand}%")
    if model:  
        filters.append("model ILIKE %s")
        values.append(f"%{model}%")
    if year_of_manufacture:
        filters.append("year_of_manufacture = %s")
        values.append(year_of_manufacture)
    if status:
        filters.append("status = %s")
        values.append(status)

    base_query = "SELECT id, brand, model, year_of_manufacture, status FROM lyfter_car_rental.cars"
    if filters:
        base_query += " WHERE " + " AND ".join(filters)

    result = db_manager.execute_query(base_query, *values)

    if result:
        cars = [
            {"id": row[0], "brand": row[1], "model": row[2], "year_of_manufacture": row[3], "status": row[4]}
            for row in result
        ]
        return jsonify(cars), 200
    else:
        return jsonify([]), 200
