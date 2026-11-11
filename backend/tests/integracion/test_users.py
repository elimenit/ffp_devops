from fastapi.testclient import TestClient
from main import app
import pytest


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


secure_password = "&&383RddpTs22%."

# SQL Injection
username_sql = "John Doe"
email_sql = "sql_injection@sqlmap.com"

# Casos Borde
lista_usuarios_borde = [
    {"username": username, "email": email, "password": password}
    for username, email, password in [
        # Casos Vacios
        ## Todos los campos vacios
        ["", "", ""],
        ## Un solo campo vacio
        ["", "test@gmail.com", secure_password],
        ["The Goat", "", secure_password],
        ["The GrandFather", "a@t.com", ""],
        ## Dos campos vacios
        ["", "", secure_password],
        ["The hacker", "", ""],
        ["", "email@hack.com", ""],
        # Inyecciones SQL
        ## 1 comilla en un solo campo
        ["'", email_sql, secure_password],
        [username_sql, "'", secure_password],
        [username_sql, email_sql, "'"],
        ## 1 comilla en dos campos
        ["'", "'", secure_password],
        ["'", email_sql, "'"],
        ## 1 comilla en todos los campos
        ["'", "'", "'"],
        ## 2 comillas en un solo campo
        ["''", email_sql, secure_password],
        [username_sql, "''", secure_password],
        [username_sql, email_sql, "''"],
        ## 2 comillas en dos campos
        ["''", "''", secure_password],
        ["''", email_sql, "''"],
        ## 2 comillas en todos los campos
        ["''", "''", "''"],
    ]
]
lista_usuarios = [
    # Casos Favorables
    {
        "username": "Yachak",
        "email": "elmeryachakhacking@gmail.com",
        "password": "pepito123",
    },
    {"username": "", "email": "", "password": ""},
]


def test_create_user(client):
    """Crear Usuarios normales no deberi fallar"""
    user = {
        "email": "example@gmail.com",
        "username": "ester",
        "password": "sdjsfdfh122ddff"
    }
    response = client.post(
        "/users",
        json=user
    )

    assert response.status_code == 201
    data = response.json()
    assert data["email"] == email
    assert data["username"] == username
    user_id = data["id"]

    response = client.delete(f"/users/{str(user_id)}")
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == email
    assert data["username"] == username
    assert user_id == data["id"]


def test_not_create_users(client):
    for user in lista_usuarios_borde:
        response = client.post(
            url="/users", headers={"Content-Type": "application/json"}, json=user
        )
        assert response.status_code == 422
