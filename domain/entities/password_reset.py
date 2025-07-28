# domain/entities/password_reset.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timedelta
from django.utils import timezone

@dataclass
class PasswordReset:
    """Entidad PasswordReset del dominio - Pura, sin dependencias"""
    id: Optional[int] = None
    user_id: int = 0
    code: int = 0
    expires_at: datetime = timezone.now() + timedelta(hours=1)
    is_used: bool = False
    created_at: datetime = timezone.now()
    updated_at: datetime = timezone.now()
    

    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.code or self.code == 0:
            raise ValueError("Code cannot be empty.")
        
        if not self.expires_at:
            raise ValueError("Expires at cannot be empty.")
        
            