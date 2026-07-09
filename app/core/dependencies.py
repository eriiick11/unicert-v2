from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_access_token, TokenExpiredError, TokenInvalidError
from app.autenticacion.repository.auth_repository import auth_repository

security = HTTPBearer(auto_error=False)

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    if credentials is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Se requiere token de acceso para este recurso")

    token = credentials.credentials

    if auth_repository.token_es_invalido(token):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="El token fue revocado")

    try:
        payload = decode_access_token(token)
    except TokenExpiredError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Sesión expirada, inicie sesión nuevamente",
        )
    except TokenInvalidError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o manipulado",
        )
    return payload

def require_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ADMINISTRADOR":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para acceder a este recurso")
    return current_user

def require_estudiante(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "ESTUDIANTE":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para acceder a este recurso")
    return current_user

def require_empresa_externa(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") != "EMPRESA_EXTERNA":
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para acceder a este recurso")
    return current_user

def require_estudiante_o_admin(current_user: dict = Depends(get_current_user)):
    if current_user.get("rol") not in ["ESTUDIANTE", "ADMINISTRADOR"]:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No tiene permisos para acceder a este recurso")
    return current_user