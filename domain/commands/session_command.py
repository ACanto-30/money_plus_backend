from dataclasses import dataclass
from datetime import datetime

@dataclass(frozen=True)
class SessionCommand:
    user_id: int
    refresh_token: str
    client_uuid: str
    token_created_at: datetime
    expires_at: datetime
