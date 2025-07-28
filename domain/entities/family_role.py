# core/domain/entities/familiesroles.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class FamilyRole:
    """Entidad FamilyRole del dominio - Pura, sin dependencias"""
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)