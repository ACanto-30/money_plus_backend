from dataclasses import dataclass
from typing import Optional
from datetime import datetime

@dataclass
class Role:
    """Entidad Role del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    name: str = ""
    description: str = ""
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    
    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.name or self.name.strip() == "":
            raise ValueError("Role name cannot be empty.")
        
        if not self.description or self.description.strip() == "":
            raise ValueError("Role description cannot be empty.") 