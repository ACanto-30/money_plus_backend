from pydantic import Field
from .base_dto import BaseDTO

class RefreshAccessTokenDTO(BaseDTO):
    """DTO para refrescar el access token"""
    refresh_token: str = Field(..., description="Token de refresco")
    client_uuid: str = Field(..., description="UUID del cliente")