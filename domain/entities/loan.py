# core/domain/entities/loan.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class Loan:
    """Entidad Loan del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    family_id: int = 0
    from_user_id: int = 0
    to_user_id: int = 0
    amount: int = 0 # en centavos
    title: str = ""
    description: str = ""
    loan_state_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


        
