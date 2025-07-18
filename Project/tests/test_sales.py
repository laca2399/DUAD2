import json

def get_user_token(client, email="user@test.com"):
    login_resp = client.post("/users/auth/login", json={"email": email, "password": "pass"})
    if login_resp.status_code == 200:
        return login_resp.json.get("token")
    
    client.post("/users/auth/register", json={"email": email, "password": "pass", "name": "User"})
    login_resp = client.post("/users/auth/login", json={"email": email, "password": "pass"})
    return login_resp.json.get("token")



def test_create_cart_success(client):
    # Arrange
    token = get_user_token(client)
    
    # Act
    resp = client.post("/sales/carts", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert resp.status_code == 201
    assert "cart_id" in resp.json

def test_add_product_to_cart_fail_insufficient_stock(client):
    # Arrange
    token = get_user_token(client)
    
    # Act
    resp = client.post("/sales/carts/1/add", json={"product_id": 1, "quantity": 1000000}, headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert resp.status_code == 400
    assert "insufficient stock" in resp.json["message"].lower()

def test_checkout_cart_fail_empty(client):
    # Arrange
    token = get_user_token(client)
    create_resp = client.post("/sales/carts", headers={"Authorization": f"Bearer {token}"})
    cart_id = create_resp.json["cart_id"]

    # Act
    checkout_resp = client.post(f"/sales/carts/{cart_id}/checkout", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert checkout_resp.status_code == 400
