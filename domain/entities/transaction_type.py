from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

@dataclass
class TransactionType:
    """Entidad TransactionType del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    name: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

class TransactionTypeEnum(Enum):
    DEPOSIT = 1
    WITHDRAW = 2
    CLEAN_BOX = 3