from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class BoxCleanUpDetail:
    """Detalle de limpieza de una caja individual, asociado a un evento de limpieza"""
    id: Optional[int] = None
    box_cleanup_event_id: int = 0
    box_id: int = 0
    amount: int = 0  # en centavos
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)