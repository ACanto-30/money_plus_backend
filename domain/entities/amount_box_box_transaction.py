from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone

@dataclass
class AmountBoxBoxTransaction:
    """Entidad AmountBoxBoxTransaction del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    box_id: int = 0
    amount_box_id: int = 0
    amount: int = 0 # en centavos
    transaction_type_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)