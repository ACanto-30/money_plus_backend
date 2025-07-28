from pydantic import BaseModel, Field
from typing import Optional
from domain.entities.box_clean_up_event import BoxCleanUpEvent
from datetime import datetime

class BoxCleanUpEventResponseDTO(BaseModel):
    id: int = Field(..., description="ID de la limpieza de caja")
    total_amount: int = Field(..., description="Cantidad total de la limpieza de caja")
    created_at: datetime = Field(..., description="Fecha de creacion de la limpieza de caja")
    updated_at: datetime = Field(..., description="Fecha de actualizacion de la limpieza de caja")

    @classmethod
    def from_entity(cls, box_clean_up_event: BoxCleanUpEvent):
        return cls(
            id=box_clean_up_event.id,
            total_amount=box_clean_up_event.total_amount,
            created_at=box_clean_up_event.created_at,
            updated_at=box_clean_up_event.updated_at
        )