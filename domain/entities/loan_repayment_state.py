from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class LoanRepaymentState:
    """Entidad LoanRepaymentState del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    state: str = ""
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)