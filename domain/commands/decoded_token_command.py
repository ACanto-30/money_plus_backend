from dataclasses import dataclass
from typing import Optional

@dataclass(frozen=True)
class DecodedTokenCommand:
    """Command para tokens JWT decodificados"""
    user_id: int
    iat: int  # Issued at (timestamp)
    exp: int  # Expiration (timestamp) 