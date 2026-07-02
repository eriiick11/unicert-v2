from pydantic import BaseModel, Field, field_validator
import re

EMAIL_REGEX = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
class LoginRequest(BaseModel):
    correo: str = Field(..., min_length=5)
    password: str = Field(..., min_length=3)

    @field_validator("correo")
    @classmethod
    def correo_valido(cls, v):
        if not re.match(EMAIL_REGEX, v):
            raise ValueError("El correo no tiene formato válido")
        return v.lower().strip()

    @field_validator("password")
    @classmethod
    def password_sin_espacios(cls, v):
        if " " in v:
            raise ValueError("La contraseña no puede contener espacios")
        return v

class UsuarioAuthData(BaseModel):
    id: int
    nombre: str
    correo: str
    rol: str

    def to_response(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "correo": self.correo,
            "rol": self.rol
        }