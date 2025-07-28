from dataclasses import dataclass

@dataclass(frozen=True)
class UserLoginCommand:
    email: str
    password: str
    client_uuid: str