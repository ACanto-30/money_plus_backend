from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BoxTransferCommand:
    """Comando para transferir dinero entre cajas"""
    user_id: int
    from_box_id: int
    to_box_id: int
    amount: int
    transaction_type_id: int
    created_at: datetime
    updated_at: datetime