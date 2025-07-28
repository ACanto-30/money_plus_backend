# core/domain/entities/sessions.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime
from django.utils import timezone

@dataclass
class Session:
    """Entidad Session del dominio - Pura, sin dependencias
    
    Nota: Solo almacena refresh tokens, NO access tokens.
    Los access tokens se validan directamente con JWT (stateless).
    """
    
    id: Optional[int] = None
    user_id: int = 0
    refresh_token: str = ""  # Solo el refresh token se almacena
    client_uuid: str = ""
    token_created_at: datetime = timezone.now()  # Momento exacto de creación del token JWT
    expires_at: Optional[datetime] = None
    is_active: bool = True  # Para poder revocar sesiones
    created_at: datetime = timezone.now()
    updated_at: datetime = timezone.now()
    
    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.user_id:
            raise ValueError("User ID cannot be empty.")
        
        if not self.refresh_token or self.refresh_token.strip() == "":
            raise ValueError("Refresh token cannot be empty.")
        
        if self.token_created_at is None:
            raise ValueError("Token creation date cannot be null.")
        
        if self.expires_at is None:
            raise ValueError("Expiration date cannot be null.")
    
    def is_expired(self) -> bool:
        """Verifica si la sesión ha expirado"""
        if self.expires_at is None:
            return True  # Si no hay fecha de expiración, considerar como expirada
        return timezone.now() > self.expires_at
    
    def revoke(self) -> None:
        """Revoca la sesión"""
        self.is_active = False
    
    def is_valid(self) -> bool:
        """Verifica si la sesión es válida (activa y no expirada)"""
        return self.is_active and not self.is_expired()
    
    def get_token_age_seconds(self) -> int:
        """Obtiene la edad del token en segundos desde su creación"""
        if self.token_created_at is None:
            return 0
        return int((timezone.now() - self.token_created_at).total_seconds())
