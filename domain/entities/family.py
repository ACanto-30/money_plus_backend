# core/domain/entities/families.py
from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class Family:
    """Entidad Family del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    name: str = ""
    family_code: str = ""
    is_active: bool = True
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.name or self.name.strip() == "":
            raise ValueError("Family name cannot be empty.")
        
        if not self.family_code or self.family_code.strip() == "":
            raise ValueError("Family code cannot be empty.")
