from pydantic import Field
from typing import Optional
from .base_dto import BaseDTO

class AuthenticationResponseDTO(BaseDTO):
    """DTO para respuesta de autenticación"""
    
    success: bool = Field(..., description="Indica si la autenticación fue exitosa")
    token: Optional[str] = Field(None, description="Token JWT de acceso")
    refresh_token: Optional[str] = Field(None, description="Token JWT de refresco")
    user_id: Optional[int] = Field(None, description="ID del usuario autenticado")
    username: Optional[str] = Field(None, description="Nombre de usuario")
    email: Optional[str] = Field(None, description="Email del usuario")
    role_id: Optional[int] = Field(None, description="ID del rol del usuario")
    message: Optional[str] = Field(None, description="Mensaje informativo")
    expires_in: Optional[int] = Field(None, description="Tiempo de expiración en segundos")

class TokenValidationDTO(BaseDTO):
    """DTO para validación de token"""
    token: str = Field(..., description="Token JWT a validar")

class TokenRefreshDTO(BaseDTO):
    """DTO para refrescar token"""
    refresh_token: str = Field(..., description="Token JWT de refresco")
    
class TokenAccessDTO(BaseDTO):
    """DTO para generar token de acceso"""
    access_token: str = Field(..., description="Token JWT de acceso")

class TokenRevokeDTO(BaseDTO):
    """DTO para revocar token"""
    token: str = Field(..., description="Token JWT a revocar")
