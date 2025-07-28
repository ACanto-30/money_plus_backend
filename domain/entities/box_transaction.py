from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class BoxTransaction:
    
    id: int = None
    box_id: int = 0
    amount: int = 0
    transaction_type_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)