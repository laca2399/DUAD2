import json

def test_register_success(client):
    # Arrange
    data = {"email": "test@example.com", "password": "1234", "name": "Test User"}
    
    # Act
    response = client.post("/users/auth/register", json=data)
    
    # Assert
    assert response.status_code == 200
    assert "token" in response.json

def test_register_missing_fields(client):
    # Arrange
    data = {"email": "test@example.com"}  # Missing password, name
    
    # Act
    response = client.post("/users/auth/register", json=data)
    
    # Assert
    assert response.status_code == 400

def test_login_success(client):
    # Arrange
    client.post("/users/auth/register", json={"email": "login@test.com", "password": "pass", "name": "User"})
    
    # Act
    response = client.post("/users/auth/login", json={"email": "login@test.com", "password": "pass"})
    
    # Assert
    assert response.status_code == 200
    assert "token" in response.json

def test_login_fail_wrong_password(client):
    # Arrange
    client.post("/users/auth/register", json={"email": "fail@test.com", "password": "pass", "name": "User"})
    
    # Act
    response = client.post("/users/auth/login", json={"email": "fail@test.com", "password": "wrongpass"})
    
    # Assert
    assert response.status_code == 401

def test_me_success(client):
    # Arrange
    client.post("/users/auth/register", json={"email": "me@test.com", "password": "pass", "name": "User"})
    login_resp = client.post("/users/auth/login", json={"email": "me@test.com", "password": "pass"})
    token = login_resp.json["token"]
    
    # Act
    response = client.get("/users/me", headers={"Authorization": f"Bearer {token}"})
    
    # Assert
    assert response.status_code == 200
    assert response.json["email"] == "me@test.com"

def test_me_no_token(client):
    # Act
    response = client.get("/users/me")
    
    # Assert
    assert response.status_code == 401
