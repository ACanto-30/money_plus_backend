from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class BoxTransactionCommand:
    """Comando para hacer una transaccion en la caja"""
    user_id: int
    box_id: int
    amount: int
    transaction_type_id: int
    created_at: datetime
    updated_at: datetime