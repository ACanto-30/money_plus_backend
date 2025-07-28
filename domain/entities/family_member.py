# core/domain/entities/familiesmembers.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class FamilyMember:
    """Entidad FamilyMember del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    family_id: int = 0
    user_id: int = 0
    is_active: bool = True
    is_banned: bool = False
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.family_id or self.family_id <= 0:
            raise ValueError("Family ID must be a positive integer.")
        
        if not self.user_id or self.user_id <= 0:
            raise ValueError("User ID must be a positive integer.")
