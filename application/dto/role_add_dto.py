from pydantic import Field
from .base_dto import BaseDTO

class RoleAddRequestDTO(BaseDTO):
    """DTO para agregar un rol"""
    name: str = Field(..., description="Nombre del rol", min_length=3, max_length=50)
    description: str = Field(..., description="Descripción del rol", min_length=3, max_length=255)