from pydantic import Field
from .base_dto import BaseDTO

class RefreshRefreshTokenDTO(BaseDTO):
    """DTO para refrescar el refresh token"""
    client_uuid: str = Field(..., description="UUID del cliente")
    refresh_token: str = Field(..., description="Token de refresco")


