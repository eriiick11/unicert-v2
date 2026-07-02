from fastapi import APIRouter, Depends, status
from fastapi.responses import JSONResponse
from fastapi.security import HTTPAuthorizationCredentials
from app.autenticacion.domain.auth import LoginRequest
from app.autenticacion.services.auth_service import (auth_service, CuentaBloqueadaError, IntentosFallidosError)
from app.core.dependencies import get_current_user, security
from app.core.responses import success_response, error_response

router = APIRouter(prefix="/api/v1/auth", tags=["Autenticación"])

@router.post("/login", status_code=status.HTTP_200_OK)
def login(data: LoginRequest):
    try:
        data_response = auth_service.login(data)
        return success_response(200, "Inicio de sesión exitoso", data_response)
    except CuentaBloqueadaError as e:
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content=error_response(
                403, "No se pudo iniciar sesión", "FORBIDDEN", str(e),
                sugerencia="Contacte al administrador para desbloquear su cuenta"
            )
        )
    except IntentosFallidosError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(
                401, "No se pudo iniciar sesión", "UNAUTHORIZED", str(e),
                intentos_restantes=e.intentos_restantes,
                sugerencia="Verifique que la tecla Mayúsculas no esté activada."
            )
        )
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(
                401, "No se pudo iniciar sesión", "UNAUTHORIZED", str(e)
            )
        )

@router.post("/logout", status_code=status.HTTP_200_OK)
def logout(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(
                401, "No se pudo cerrar la sesión", "UNAUTHORIZED",
                "Se requiere token de acceso para cerrar sesión"
            )
        )
    try:
        auth_service.logout(credentials.credentials)
        return success_response(200, "Sesión cerrada correctamente", None)
    except ValueError as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content=error_response(401, "No se pudo cerrar sesión", "UNAUTHORIZED", str(e))
        )

@router.get("/me", status_code=status.HTTP_200_OK)
def get_me(current_user: dict = Depends(get_current_user)):
    data = auth_service.get_me(current_user)
    return success_response(200, "Usuario autenticado", data)

@router.get("/validar", status_code=status.HTTP_200_OK)
def validar_token(current_user: dict = Depends(get_current_user)):
    data = auth_service.validar_token(current_user)
    return success_response(200, "Token válido", data)