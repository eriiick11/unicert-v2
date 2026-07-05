import pytest
from fastapi.testclient import TestClient

from main import app
from app.core.security import hash_password, create_access_token
from app.usuarios.domain.usuarios import User
from app.usuarios.repository.usuario_repo import UserRepository
from app.autenticacion.repository.auth_repository import auth_repository


@pytest.fixture(autouse=True)
def reset_stores():
    UserRepository.clear()
    auth_repository._tokens_invalidados.clear()

    admin = User(
        id=1,
        nombre="Admin UniCert",
        correo="admin@unicert.com",
        password=hash_password("admin123"),
        rol="ADMINISTRADOR",
        activo=True,
    )
    UserRepository._users.append(admin)
    UserRepository._next_id = 2
    UserRepository._seeded = True

    yield


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def token_admin():
    return create_access_token({
        "id": 1,
        "correo": "admin@unicert.com",
        "rol": "ADMINISTRADOR",
        "nombre": "Admin UniCert",
    })


@pytest.fixture
def auth_headers(token_admin):
    return {"Authorization": f"Bearer {token_admin}"}


@pytest.fixture
def inactive_user():
    user = User(
        id=UserRepository._next_id,
        nombre="Inactivo",
        correo="inactivo@test.com",
        password=hash_password("pass123"),
        rol="ESTUDIANTE",
        activo=False,
    )
    UserRepository._users.append(user)
    UserRepository._next_id += 1
    return user


@pytest.fixture
def unregistered_email():
    return "nadie@test.com"
