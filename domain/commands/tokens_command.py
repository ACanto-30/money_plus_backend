from dataclasses import dataclass

@dataclass(frozen=True)
class TokensCommand:
    refresh_token: str
    access_token: str
