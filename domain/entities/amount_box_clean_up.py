from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone


@dataclass
class AmountBoxCleanUp:
    """Evento de limpieza de una caja de dinero"""
    id: Optional[int] = None
    total_amount: int = 0  # en centavos
    amount_box_id: Optional[int] = None
    box_cleanup_event_id: Optional[int] = None
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)
