import re
from datetime import datetime, timezone
from pydantic import BaseModel, ConfigDict

UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

ESTADOS_CERTIFICADO = frozenset({"DISPONIBLE", "ANULADO"})

class CertificadoVerificacion:
    def __init__(self, uuid: str, estudiante: str, tipo_certificado: str, fecha_emision: str, 
                 estado: str = "DISPONIBLE",hash_archivo: str = None):
        self.uuid = uuid
        self.estudiante = estudiante
        self.tipo_certificado = tipo_certificado
        self.fecha_emision = fecha_emision
        self.estado = estado
        self.hash_archivo = hash_archivo

    def es_valido(self) -> bool:
        return self.estado == "DISPONIBLE"

    def esta_anulado(self) -> bool:
        return self.estado == "ANULADO"

    def verificar_integridad(self, hash_recalculado: str) -> bool:
        return self.hash_archivo == hash_recalculado

    def to_verificacion_valida(self) -> dict:
        return {
            "valido": True,
            "uuid": self.uuid,
            "estudiante": self.estudiante,
            "tipo_certificado": self.tipo_certificado,
            "fecha_emision": self.fecha_emision,
            "estado": "VIGENTE",
        }

    def to_verificacion_anulada(self) -> dict:
        return {
            "valido": False,
            "uuid": self.uuid,
            "estado": "ANULADO",
        }

    def to_integridad(self, integro: bool) -> dict:
        return {
            "uuid": self.uuid,
            "integro": integro,
            "fecha_emision": self.fecha_emision,
            "mensaje": (
                "El documento no ha sido alterado desde su emisión"
                if integro else
                "El documento ha sido modificado y no es confiable"
            ),
        }

class Verificacion:
    def __init__(self, id: int, uuid_consultado: str, ip_verificador: str):
        self.id = id
        self.uuid_consultado = uuid_consultado
        self.ip_verificador = ip_verificador
        self.timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")

    def to_response(self) -> dict:
        return {
            "id": self.id,
            "uuid_consultado": self.uuid_consultado,
            "ip_verificador": self.ip_verificador,
            "timestamp": self.timestamp,
        }

class VerificacionResponse(BaseModel):
    id: int
    uuid_consultado: str
    ip_verificador: str
    timestamp: str

    model_config = ConfigDict(from_attributes=True)