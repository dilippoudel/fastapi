from app import schemas
from .database import client, session # noqa
import pytest
import jwt
from app.config import settings
@pytest.fixture
def test_user(client):
    user_data = {"email": "hello123@gmail.com", "password": "password123"}
    res = client.post("/users", json=user_data)
    assert res.status_code == 201
    print(res.json())
    new_user = res.json()
    new_user['password'] = user_data["password"]
    return new_user


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