import re
from pydantic import BaseModel, ConfigDict

ESTADOS_REPOSITORIO = frozenset({"GENERADO", "DISPONIBLE", "ANULADO"})

UUID_REGEX = re.compile(r"^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$", re.IGNORECASE)

class CertificadoRepositorio:
    def __init__(self, uuid: str, certificado_id: int, usuario_id: int,
                 tipo_certificado: str, fecha_emision: str,
                 estado: str, ruta_archivo: str):
        self.uuid = uuid
        self.certificado_id = certificado_id
        self.usuario_id = usuario_id
        self.tipo_certificado = tipo_certificado
        self.fecha_emision = fecha_emision
        self.estado = estado
        self.ruta_archivo = ruta_archivo

    def esta_anulado(self) -> bool:
        return self.estado == "ANULADO"

    def pertenece_a(self, usuario_id: int) -> bool:
        return self.usuario_id == usuario_id

    def tiene_estado_valido(self) -> bool:
        return self.estado in ESTADOS_REPOSITORIO

    def to_response(self) -> dict:
        return {
            "uuid": self.uuid,
            "certificado_id": self.certificado_id,
            "fecha_emision": self.fecha_emision,
            "estado": self.estado,
            "ruta_archivo": self.ruta_archivo,
        }

    def to_history_item(self) -> dict:
        return {
            "uuid": self.uuid,
            "certificado_id": self.certificado_id,
            "tipo_certificado": self.tipo_certificado,
            "fecha_emision": self.fecha_emision,
            "estado": self.estado,
        }

    def to_metadata(self) -> dict:
        return {
            "uuid": self.uuid,
            "tipo_certificado": self.tipo_certificado,
            "fecha_emision": self.fecha_emision,
            "estado": self.estado,
        }

class CertificateRepositoryResponse(BaseModel):
    uuid: str
    certificado_id: int
    fecha_emision: str
    estado: str
    ruta_archivo: str

    model_config = ConfigDict(from_attributes=True)

class CertificateHistoryItem(BaseModel):
    uuid: str
    certificado_id: int
    tipo_certificado: str
    fecha_emision: str
    estado: str

    model_config = ConfigDict(from_attributes=True)

class CertificateMetadataResponse(BaseModel):
    uuid: str
    tipo_certificado: str
    fecha_emision: str
    estado: str

    model_config = ConfigDict(from_attributes=True)