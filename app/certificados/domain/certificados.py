from pydantic import BaseModel, ConfigDict, Field
from typing import Optional

class Certificate:
    def __init__(self, id: int, uuid: str, solicitud_id: int, plantilla_id: int,
                 estado: str = "GENERADO", fecha_emision: str = None,
                 ruta_pdf: str = None, nombre_estudiante: str = None):
        self.id = id
        self.uuid = uuid
        self.solicitud_id = solicitud_id
        self.plantilla_id = plantilla_id
        self.estado = estado
        self.fecha_emision = fecha_emision
        self.ruta_pdf = ruta_pdf
        self.nombre_estudiante = nombre_estudiante

    def esta_anulado(self) -> bool:
        return self.estado == "ANULADO"

    def to_response(self) -> dict:
        data = {
            "id": self.id,
            "uuid": self.uuid,
            "solicitud_id": self.solicitud_id,
            "plantilla_id": self.plantilla_id,
            "estado": self.estado,
            "fecha_emision": self.fecha_emision,
            "ruta_pdf": self.ruta_pdf, 
        }
        if self.nombre_estudiante:
            data["estudiante"] = {
                "nombre": self.nombre_estudiante
            }
        return data

    def to_anulado_response(self) -> dict:
        estudiante = {}
        if self.nombre_estudiante:
            estudiante = {
                "nombre": self.nombre_estudiante,
            }
        return {
            "id": self.id,
            "uuid": self.uuid,
            "estado": self.estado,
            "fecha_emision": self.fecha_emision,
            "estudiante": estudiante,
        }

class CertificateCreate(BaseModel):
    solicitud_id: int = Field(..., gt=0)

class CertificateResponse(BaseModel):
    id: int
    uuid: str
    solicitud_id: int
    plantilla_id: int
    estado: str
    fecha_emision: str
    ruta_pdf: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)

class CertificateAnuladoResponse(BaseModel):
    id: int
    uuid: str
    estado: str
    fecha_emision: str
    estudiante: dict = Field(default_factory=dict)
