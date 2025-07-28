from dataclasses import dataclass

@dataclass(frozen=True)
class AccessTokenPayloadCommand:
    user_id: int
    username: str
    email: str
    role_id: int
    client_uuid: str
