from datetime import datetime, timedelta, timezone

import pytest
from jose import jwt

from app.autenticacion.repository.auth_repository import MAX_INTENTOS
from app.core.security import SECRET_KEY


class TestLogin:

    LOGIN_URL = "/api/v1/auth/login"

    def test_login_admin_success(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "admin@unicert.com",
            "password": "admin123",
        })
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["statusCode"] == 200
        assert body["message"] == "Inicio de sesión exitoso"
        assert "token" in body["data"]
        assert body["data"]["tipo_token"] == "Bearer"
        assert body["data"]["usuario"]["correo"] == "admin@unicert.com"
        assert body["data"]["usuario"]["rol"] == "ADMINISTRADOR"

    def test_login_email_case_insensitive(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "ADMIN@UNICERT.COM",
            "password": "admin123",
        })
        assert response.status_code == 200

    def test_login_invalid_email_format(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "no-es-un-email",
            "password": "admin123",
        })
        assert response.status_code == 400

    def test_login_empty_password(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "admin@unicert.com",
            "password": "a",
        })
        assert response.status_code == 400

    def test_login_unregistered_email(self, client, unregistered_email):
        response = client.post(self.LOGIN_URL, json={
            "correo": unregistered_email,
            "password": "admin123",
        })
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert "Correo no registrado" in body["error"]["details"]

    def test_login_wrong_password(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "admin@unicert.com",
            "password": "wrongpass",
        })
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert body["error"]["error_code"] == "UNAUTHORIZED"
        assert "Contraseña incorrecta" in body["error"]["details"]
        assert "intentos_restantes" in body["error"]

    def test_login_block_after_max_attempts(self, client):
        wrong = {"correo": "admin@unicert.com", "password": "wrongpass"}

        for i in range(MAX_INTENTOS - 1):
            r = client.post(self.LOGIN_URL, json=wrong)
            assert r.status_code == 401
            assert r.json()["error"]["intentos_restantes"] == MAX_INTENTOS - (i + 1)

        r_final = client.post(self.LOGIN_URL, json=wrong)
        assert r_final.status_code == 403
        body = r_final.json()
        assert body["error"]["error_code"] == "FORBIDDEN"
        assert "bloqueada" in body["error"]["details"].lower()

    def test_login_correct_after_wrong_resets_counter(self, client):
        wrong = {"correo": "admin@unicert.com", "password": "wrongpass"}
        correct = {"correo": "admin@unicert.com", "password": "admin123"}

        for _ in range(3):
            client.post(self.LOGIN_URL, json=wrong)

        r = client.post(self.LOGIN_URL, json=correct)
        assert r.status_code == 200

        r = client.post(self.LOGIN_URL, json=wrong)
        assert r.status_code == 401
        assert r.json()["error"]["intentos_restantes"] == MAX_INTENTOS - 1

    def test_login_inactive_user(self, client, inactive_user):
        response = client.post(self.LOGIN_URL, json={
            "correo": "inactivo@test.com",
            "password": "pass123",
        })
        assert response.status_code == 401
        body = response.json()
        assert "inactiva" in body["error"]["details"].lower()

    def test_login_password_with_spaces_validated(self, client):
        response = client.post(self.LOGIN_URL, json={
            "correo": "admin@unicert.com",
            "password": "pass with spaces",
        })
        assert response.status_code == 400


class TestLogout:

    LOGOUT_URL = "/api/v1/auth/logout"

    def test_logout_success(self, client, auth_headers):
        response = client.post(self.LOGOUT_URL, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["message"] == "Sesión cerrada correctamente"

    def test_logout_no_token(self, client):
        response = client.post(self.LOGOUT_URL)
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False
        assert "token" in body["error"]["details"].lower()

    def test_logout_revoked_token(self, client, auth_headers):
        client.post(self.LOGOUT_URL, headers=auth_headers)
        response = client.post(self.LOGOUT_URL, headers=auth_headers)
        assert response.status_code == 401
        body = response.json()
        assert "no es válido" in body["error"]["details"].lower()


class TestGetMe:

    ME_URL = "/api/v1/auth/me"

    def test_get_me_success(self, client, auth_headers):
        response = client.get(self.ME_URL, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["correo"] == "admin@unicert.com"
        assert body["data"]["rol"] == "ADMINISTRADOR"

    def test_get_me_no_token(self, client):
        response = client.get(self.ME_URL)
        assert response.status_code == 401
        body = response.json()
        assert body["success"] is False

    def test_get_me_revoked_token(self, client, auth_headers, token_admin):
        client.post("/api/v1/auth/logout", headers=auth_headers)
        response = client.get(self.ME_URL, headers=auth_headers)
        assert response.status_code == 401
        body = response.json()
        assert "revocado" in body["error"]["details"].lower()


class TestValidarToken:

    VALIDAR_URL = "/api/v1/auth/validar"

    def test_validar_token_success(self, client, auth_headers):
        response = client.get(self.VALIDAR_URL, headers=auth_headers)
        assert response.status_code == 200
        body = response.json()
        assert body["success"] is True
        assert body["data"]["correo"] == "admin@unicert.com"

    def test_validar_token_no_token(self, client):
        response = client.get(self.VALIDAR_URL)
        assert response.status_code == 401

    def test_validar_token_revoked(self, client, auth_headers):
        client.post("/api/v1/auth/logout", headers=auth_headers)
        response = client.get(self.VALIDAR_URL, headers=auth_headers)
        assert response.status_code == 401
        body = response.json()
        assert "revocado" in body["error"]["details"].lower()

    def test_validar_token_expired(self, client):
        expired_token = jwt.encode(
            {
                "id": 1,
                "correo": "admin@unicert.com",
                "rol": "ADMINISTRADOR",
                "nombre": "Admin UniCert",
                "exp": datetime.now(timezone.utc) - timedelta(hours=1),
            },
            SECRET_KEY,
            algorithm="HS256",
        )
        headers = {"Authorization": f"Bearer {expired_token}"}
        response = client.get(self.VALIDAR_URL, headers=headers)
        assert response.status_code == 401
        body = response.json()
        assert "expirada" in body["error"]["details"].lower()

    def test_validar_token_invalid_signature(self, client):
        headers = {"Authorization": "Bearer token-invalido"}
        response = client.get(self.VALIDAR_URL, headers=headers)
        assert response.status_code == 401
        body = response.json()
        assert body["error"]["details"] == "Token inválido o manipulado"
