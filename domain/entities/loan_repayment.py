# core/domain/entities/loan_repayment.py

from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class LoanRepayment:
    """Entidad LoanRepayment del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    loan_id: Optional[int] = None
    user_id: Optional[int] = None
    amount: float = 0.0
    title: str = ""
    description: str = ""
    loan_repayment_state_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)