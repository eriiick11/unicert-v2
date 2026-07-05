from typing import Optional
from pydantic import BaseModel, Field, field_validator

class Plantilla:
    def __init__(self, id: int, nombre: str, tipo_certificado: str, 
                 estructura: list, activa: bool = True):
        self.id = id
        self.nombre = nombre
        self.tipo_certificado = tipo_certificado
        self.estructura = estructura
        self.activa = activa

    def to_response(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_certificado": self.tipo_certificado,
            "estructura": self.estructura,
            "activa": self.activa
        }

    def to_response_lista(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "tipo_certificado": self.tipo_certificado,
            "activa": self.activa
        }

class PlantillaCreate(BaseModel):
    nombre: str = Field(..., min_length=1)
    tipo_certificado: str = Field(..., min_length=1)
    estructura: dict = Field(..., json_schema_extra={"example": {"campos": ["nombre_estudiante", "programa_academico", "fecha_emision"]}})

    @field_validator("estructura")
    @classmethod
    def validar_estructura(cls, v):
        if not isinstance(v, dict) or "campos" not in v:
            raise ValueError("La estructura debe tener la clave 'campos'")
        if not isinstance(v["campos"], list) or len(v["campos"]) == 0:
            raise ValueError("La plantilla debe tener al menos un campo dinámico")
        return v
    
class PlantillaUpdate(BaseModel):
    nombre: Optional[str] = Field(None, min_length=1)
    tipo_certificado: Optional[str] = Field(None, min_length=1)
    estructura: Optional[dict] = Field(None, json_schema_extra={"example": {"campos": ["nombre_estudiante", "programa_academico", "fecha_emision"]}})

    @field_validator("estructura")
    @classmethod
    def validar_estructura(cls, v):
        if not isinstance(v, dict) or "campos" not in v:
            raise ValueError("La plantilla debe tener al menos un campo dinámico")
        if not isinstance(v["campos"], list) or len(v["campos"]) == 0:
            raise ValueError("La plantilla debe tener al menos un campo dinámico")
        return v
    
class PlantillaResponse(BaseModel):
    id: int 
    nombre: str
    tipo_certificado: str
    estructura: list
    activa: bool