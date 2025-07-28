from pydantic import Field
from .base_dto import BaseDTO

class UserLoginDTO(BaseDTO):
    """DTO para login de usuarios"""
    
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    password: str = Field(..., min_length=6, max_length=100)
    client_uuid: str = Field(..., min_length=36, max_length=36)
    