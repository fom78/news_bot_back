# tests/auth/test_auth_routes.py
import pytest
from app.extensions import db
from app.auth.models import User

# Datos de prueba
PHONE = "+123456789"
PASSWORD = "password123"

def test_register_success(test_client):
    response = test_client.post("api/auth/register", json={
        "phone_number": PHONE,
        "password": PASSWORD
    })

    data = response.get_json()

    assert response.status_code == 201
    assert data["message"] == "Usuario registrado exitosamente"
    assert data["phone_number"] == PHONE

    # Aseguramos que el usuario quedó en la DB
    user = User.query.filter_by(phone_number=PHONE).first()
    assert user is not None
    assert user.phone_number == PHONE

def test_register_existing_user(test_client):
    # Intentamos registrar el mismo número otra vez
    response = test_client.post("api/auth/register", json={
        "phone_number": PHONE,
        "password": "otra_pass"
    })

    data = response.get_json()

    assert response.status_code == 400
    assert data["error"]["message"] == "El número está registrado"

def test_register_invalid_data(test_client):
    # Faltan campos
    response = test_client.post("api/auth/register", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"]["message"] == "Datos inválidos"
    assert "phone_number" in data["error"]["details"]

def test_login_success(test_client):
    response = test_client.post("api/auth/login", json={
        "phone_number": PHONE,
        "password": PASSWORD
    })

    data = response.get_json()

    assert response.status_code == 200
    assert "access_token" in data
    assert data["user"]["phone_number"] == PHONE

def test_login_invalid_credentials(test_client):
    response = test_client.post("api/auth/login", json={
        "phone_number": PHONE,
        "password": "wrongpass"
    })

    data = response.get_json()

    assert response.status_code == 401
    assert data["error"]["message"] == "Credenciales inválidas"

def test_login_missing_fields(test_client):
    response = test_client.post("api/auth/login", json={})
    data = response.get_json()

    assert response.status_code == 400
    assert data["error"]["message"] == "Datos inválidos"
