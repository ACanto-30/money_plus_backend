from pydantic import field_validator, Field
from .base_dto import BaseDTO

class UserRegistrationDTO(BaseDTO):
    """DTO para registro de usuarios"""
    
    username: str = Field(..., min_length=3, max_length=50, pattern="^[a-zA-Z0-9_]+$")
    password: str = Field(..., min_length=6, max_length=100)
    email: str = Field(..., pattern=r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
    role_id: int = Field(..., gt=0)
    client_uuid: str = Field(..., min_length=36, max_length=36)
    
    
    @field_validator('username')
    @classmethod
    def validate_username(cls, v: str) -> str:
        reserved_words = ['admin', 'root', 'system', 'test']
        if v.lower() in reserved_words:
            raise ValueError('El username no puede ser una palabra reservada')
        return v