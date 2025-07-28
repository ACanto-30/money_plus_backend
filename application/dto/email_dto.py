from pydantic import Field, EmailStr
from typing import List, Optional
from .base_dto import BaseDTO

class EmailMessageDTO(BaseDTO):
    """DTO para mensaje de email"""
    to: EmailStr = Field(..., description="Email del destinatario")
    subject: str = Field(..., min_length=1, max_length=255, description="Asunto del email")
    body: str = Field(..., min_length=1, description="Cuerpo del mensaje en texto plano")
    cc: Optional[List[EmailStr]] = Field(None, description="Destinatarios en copia")
    bcc: Optional[List[EmailStr]] = Field(None, description="Destinatarios en copia oculta")
    html_body: Optional[str] = Field(None, description="Cuerpo del mensaje en HTML")

class EmailResultDTO(BaseDTO):
    """DTO para resultado del envío de email"""
    success: bool = Field(..., description="Indica si el envío fue exitoso")
    message_id: Optional[str] = Field(None, description="ID del mensaje enviado")
    error_message: Optional[str] = Field(None, description="Mensaje de error si falló")

class BulkEmailRequestDTO(BaseDTO):
    """DTO para solicitud de envío masivo de emails"""
    emails: List[EmailMessageDTO] = Field(..., min_items=1, description="Lista de emails a enviar")

class BulkEmailResponseDTO(BaseDTO):
    """DTO para respuesta de envío masivo de emails"""
    results: List[EmailResultDTO] = Field(..., description="Resultados del envío de cada email")
    total_sent: int = Field(..., description="Total de emails enviados exitosamente")
    total_failed: int = Field(..., description="Total de emails que fallaron")