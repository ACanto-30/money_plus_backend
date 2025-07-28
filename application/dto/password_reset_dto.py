from pydantic import Field
from .base_dto import BaseDTO

class PasswordResetRequestDTO(BaseDTO):
    """DTO para solicitud de reseteo de contraseña"""
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')

class PasswordResetDTO(BaseDTO):
    """DTO para reseteo de contraseña"""
    code: int = Field(..., description="Código de reseteo")
    new_password: str = Field(..., description="Nueva contraseña")
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
