from flask import Flask, request, jsonify
import json
from users_and_authentication import check_admin_role

PRODUCTS_FILE = "products.json"

def read_products():
    try:
        with open(JSON_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_products(products):
    with open(JSON_FILE, "w") as file:
        json.dump(products, file, indent=4)



@app.route("/products", methods=["GET"])
def products():
    products_list = read_products()
    availability_filter = request.args.get("availability")
    category_filter = request.args.get("category")

    if availability_filter:
        products_list = [product for product in products_list if product["availability"] == availability_filter]

    if category_filter:
        products_list = [product for product in products_list if product["category"] == category_filter]

    return jsonify({"data": products_list})

@app.route("/products", methods=["POST"])
def add_product():
    admin_check = check_admin_role
    if admin_check:
        return admin_check
    
    products_list = read_products()
    new_product = request.json

    if not all(key in new_product for key in ["product_id", "name", "description", "availability", "category", "price", "quantity"]):
        return jsonify({"error": "Mandatory Fields are missing."}), 400
    
    if any(product["product_id"] == new_product["product_id"] for product in products_list):
        return jsonify({"error": "The identifier already exists."}), 400
    
    if new_product["availability"] not in ["Available", "Out of Stock", "Pre-order"]:
        return jsonify({"error": "The status is invalid."}), 400
    
    products_list.append(new_product)
    write_products(products_list)
    return jsonify({"message": "Product created successfully.", "product": new_product}), 201

@app.route("/products/<int:product_id>", methods=["PUT"])
def update_product(product_id):
    admin_check = check_admin_role()
    if admin_check:
        return admin_check
    
    products_list = read_products()
    updated_data = request.json

    for product in products_list:
        if product["product_id"] == product_id:
            product.update(updated_data)
            write_products(products_list)
            return jsonify({"message": "Product updated successfully.", "product": product}), 200

    return jsonify({"error": "Product not found."}), 404

@app.route("/products/<int:product_id>", methods=["DELETE"])
def delete_product(product_id):
    admin_check = check_admin_role()
    if admin_check:
        return admin_check
    
    products_list = read_products()

    for product in products_list:
        if product["product_id"] == product_id:
            products_list.remove(product)
            write_products(products_list)
            return jsonify({"message": "Product deleted successfully."}), 200

    return jsonify({"error": "Product not found."}), 404


def update_product_stock(product_id, quantity_sold):
    
    products_list = read_products(PRODUCTS_FILE)
    for product in products_list:
        if product["product_id"] == product_id:
            if product["stock"] >= quantity_sold:
                product["stock"] -= quantity_sold
                write_products(PRODUCTS_FILE, products_list)  
                return True
            else:
                return False  
    return False  