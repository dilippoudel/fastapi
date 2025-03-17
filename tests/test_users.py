from app import schemas
import jwt
from app.config import settings
import pytest

"""Test to create users."""



def test_create_user(client):
    res = client.post("/users/", json={"email":"hello123@gmail.com", "password":"password123"})
    new_user = schemas.UserOut(**res.json())
    assert new_user.email == "hello123@gmail.com"
    assert res.status_code == 201

"""Test for user log in"""
def test_login_user(client, test_user):
    res = client.post("/login", data={"username": test_user['email'], "password": test_user['password']})
    login_response = schemas.Token(**res.json())
    payload = jwt.decode(login_response.access_token, settings.secret_key, algorithms=[settings.algorithm])
    id = payload.get("user_id")
    assert id == test_user['id']
    assert login_response.token_type == "Bearer"
    assert res.status_code == 200

"""Test for invalid credentials."""
@pytest.mark.parametrize("email, password, status_code", [
    ('hello123@gmail.com', 'pass12345', 403),
    ('hello143@gmail.com', 'passworuuud123', 403),
    ('hedili123@gmail.com', 'pass12345', 403),
    (None, 'pass12345', 403),
    ('hello123@gmail.com', None, 403)
])
def test_incorrect_login(test_user, client,  email, password, status_code):
    res = client.post('/login', data={"username": email, "password": password})
    assert res.status_code == status_code
