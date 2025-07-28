# core/domain/entities/user.py
from dataclasses import dataclass
from typing import Optional
from ..value_objects.email import Email
from datetime import datetime
from django.utils import timezone

@dataclass
class User:
    """Entidad User del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    username: str = ""
    password: str = ""
    email: Email = None
    role_id: int = 0
    created_at: datetime = timezone.now()
    updated_at: datetime = timezone.now()
    
    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.username or self.username.strip() == "":
            raise ValueError("Username cannot be empty.")
        
        if not self.password or self.password.strip() == "":
            raise ValueError("Password cannot be empty.")
        
        if self.email is None:
            raise ValueError("Email cannot be null.")