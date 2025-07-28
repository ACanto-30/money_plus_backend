from dataclasses import dataclass

@dataclass(frozen=True)
class UserRegistrationCommand:
    username: str
    email: str
    password: str
    role_id: int
    client_uuid: str