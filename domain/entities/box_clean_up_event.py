from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class BoxCleanUpEvent:
    """Evento de limpieza de cajas (agrupa varias limpiezas de cajas individuales)"""
    id: Optional[int] = None
    total_amount: int = 0  # en centavos
    user_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)


