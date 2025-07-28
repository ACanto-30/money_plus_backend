from dataclasses import dataclass
from datetime import datetime, timezone

@dataclass
class CleanUpSchedule:
    id: int
    user_id: int
    clean_up_day_interval: int
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    