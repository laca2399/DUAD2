import json, uuid

def get_admin_token(client):
    # Arrange
    login_resp = client.post("/users/auth/login", json={"email": "admin@test.com", "password": "adminpassword"})
    if login_resp.status_code == 200:
        return login_resp.json.get("token")
    return None

def test_create_product_success(client):
    # Arrange
    token = get_admin_token(client)
    if not token:
        return
    sku = str(uuid.uuid4())
    data = {
        "name": "Dog Food",
        "sku": sku,
        "description": "Tasty food for dogs",
        "price": 19.99,
        "quantity": 10,
        "category_id": 1,
        "availability_id": 1
    }
    
    # Act
    response = client.post("/products/products", json=data, headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    assert response.json["name"] == "Dog Food"

def test_create_product_forbidden(client):

    # Arrange
    sku = str(uuid.uuid4())
    data = {
        "name": "Cat Toy",
        "sku": sku,
        "description": "Fun toy for cats",
        "price": 9.99,
        "quantity": 5,
        "category_id": 1,
        "availability_id": 1
    }
    
    # Act
    response = client.post("/products/products", json=data)
    
    # Assert
    assert response.status_code == 403

def test_list_products_cache(client):
    # Act
    response = client.get("/products/products")
    
    # Assert
    assert response.status_code == 200
    assert isinstance(response.json, list)

def test_get_product_not_found(client):
    # Act
    response = client.get("/products/products/99999")
    
    # Assert
    assert response.status_code == 404

def test_update_product_success(client):
    # Arrange
    token = get_admin_token(client)
    if not token:
        return
    sku = str(uuid.uuid4())
    create_resp = client.post("/products/products", json={
        "name": "Bird Seed",
        "sku": sku,
        "description": "Healthy bird seed",
        "price": 5.99,
        "quantity": 50,
        "category_id": 1,
        "availability_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    product_id = create_resp.json["id"]

    # Act
    update_resp = client.put(f"/products/products/{product_id}", json={"quantity": 40}, headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert update_resp.status_code == 200
    assert update_resp.json["message"] == "Product updated"

def test_delete_product_success(client):
    # Arrange
    token = get_admin_token(client)
    if not token:
        return
    sku = str(uuid.uuid4())
    create_resp = client.post("/products/products", json={
        "name": "Fish Food",
        "sku": sku,
        "description": "For fish",
        "price": 3.99,
        "quantity": 30,
        "category_id": 1,
        "availability_id": 1
    }, headers={"Authorization": f"Bearer {token}"})
    product_id = create_resp.json["id"]

    # Act
    delete_resp = client.delete(f"/products/products/{product_id}", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert delete_resp.status_code == 200
    assert delete_resp.json["message"] == "Product deleted"