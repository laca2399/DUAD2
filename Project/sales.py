from flask import Flask, request, jsonify
import json, secrets
from products import update_product_stock

CARTS_FILE = "carts.json"
SALES_FILE = "sales.json"
INVOICES_FILE = "invoices.json"
PRODUCTS_FILE = "products.json"

def read_data(filename):
    try:
        with open(filename, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def write_data(filename, data):
    with open(filename, "w") as file:
        json.dump(data, file, indent=4)

def check_product_stock(product_id, quantity):
    products_list = read_data(PRODUCTS_FILE)
    for product in products_list:
        if product["product_id"] == product_id:
            if product["availability"] == "Available" and quantity <= product["stock"]:
                return product
    return None

@app.route("/carts", methods=["POST"])
def create_cart():
    cart_id = secrets.token_hex(16)  
    cart = {"cart_id": cart_id, "products": []}
    carts = read_data(CARTS_FILE)
    carts.append(cart)
    write_data(CARTS_FILE, carts)
    return jsonify({"message": "Cart created", "cart_id": cart_id}), 201

@app.route("/carts/<cart_id>/add", methods=["POST"])
def add_to_cart(cart_id):
    cart = next((c for c in read_data(CARTS_FILE) if c["cart_id"] == cart_id), None)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404
    
    product_data = request.json
    product_id = product_data.get("product_id")
    quantity = product_data.get("quantity", 1)
    
    product = check_product_stock(product_id, quantity)
    if not product:
        return jsonify({"error": "Product not available or insufficient stock"}), 400
    
    cart["products"].append({"product_id": product_id, "quantity": quantity})
    write_data(CARTS_FILE, read_data(CARTS_FILE))  # Save updated carts
    return jsonify({"message": "Product added to cart"}), 200

@app.route("/carts/<cart_id>/remove", methods=["POST"])
def remove_from_cart(cart_id):
    cart = next((c for c in read_data(CARTS_FILE) if c["cart_id"] == cart_id), None)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404
    
    product_id = request.json.get("product_id")
    cart["products"] = [p for p in cart["products"] if p["product_id"] != product_id]
    write_data(CARTS_FILE, read_data(CARTS_FILE))
    return jsonify({"message": "Product removed from cart"}), 200

@app.route("/carts/<cart_id>/checkout", methods=["POST"])
def checkout(cart_id):
    cart = next((c for c in read_data(CARTS_FILE) if c["cart_id"] == cart_id), None)
    if not cart:
        return jsonify({"error": "Cart not found"}), 404
    
    invoice_id = secrets.token_hex(16)  
    invoice = {"invoice_id": invoice_id, "cart_id": cart_id, "products": cart["products"], "status": "Paid"}
    
    for item in cart["products"]:
        if not update_product_stock(item["product_id"], item["quantity"]):
            return jsonify({"error": "Not enough stock for product ID " + str(item["product_id"])}), 400
    
    sales = read_data(SALES_FILE)
    sales.append(invoice)
    write_data(SALES_FILE, sales)
    
    return jsonify({"message": "Checkout successful", "invoice_id": invoice_id}), 200
    

@app.route("/invoices/<invoice_id>", methods=["GET"])
def get_invoice(invoice_id):
    invoices = read_data(INVOICES_FILE)
    invoice = next((i for i in invoices if i["invoice_id"] == invoice_id), None)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    return jsonify(invoice)

@app.route("/invoices/<invoice_id>/return", methods=["POST"])
def return_product(invoice_id):
    invoices = read_data(INVOICES_FILE)
    invoice = next((i for i in invoices if i["invoice_id"] == invoice_id), None)
    if not invoice:
        return jsonify({"error": "Invoice not found"}), 404
    
    products_list = read_data(PRODUCTS_FILE)
    for item in invoice["products"]:
        product = next((p for p in products_list if p["product_id"] == item["product_id"]), None)
        if product:
            product["stock"] += item["quantity"]
    
    write_data(PRODUCTS_FILE, products_list)
    
    return jsonify({"message": "Return processed, stock updated"}), 200

