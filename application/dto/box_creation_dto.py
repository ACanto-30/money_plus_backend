from pydantic import BaseModel, Field
from typing import Optional
from domain.entities.box import Box

class BoxCreationRequestDTO(BaseModel):
    name : str = Field(..., description="Nombre de la caja")

class BoxCreationResponseDTO(BaseModel):
    id: int = Field(..., description="ID de la caja")
    name: str = Field(..., description="Nombre de la caja")
    amount: int = Field(..., description="Cantidad de la caja")

    @classmethod
    def from_entity(cls, box: Box):
        return cls(
            id=box.id,
            name=box.name,
            amount=box.amount
        )

class BoxRenameRequestDTO(BaseModel):
    name: str = Field(..., description="Nombre de la caja")

    @classmethod
    def from_entity(cls, box: Box):
        return cls(
            name=box.name
        )