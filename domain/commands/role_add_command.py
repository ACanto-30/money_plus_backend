from dataclasses import dataclass

@dataclass(frozen=True)
class RoleAddCommand:
    name: str
    description: str
