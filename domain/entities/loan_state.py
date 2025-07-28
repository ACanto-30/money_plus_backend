# domain/entities/loan_state.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from enum import Enum

@dataclass
class LoanState:
    """Entidad LoanState del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    state: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


class LoanStateEnum(Enum):
    """Enum para los estados de un prestamo"""
    PENDING = 1
    REJECT = 2
    IN_PROGRESS = 3
    PAID = 4