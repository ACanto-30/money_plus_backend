from pydantic import BaseModel, Field
from domain.entities.saving_box import SavingBox

class SavingBoxResponseDTO(BaseModel):
    id: int = Field(..., description="ID de la caja de ahorro")
    amount: int = Field(..., description="Cantidad total de la caja de ahorro")
    
    @classmethod
    def from_entity(cls, saving_box: SavingBox):
        return cls(
            id=saving_box.id,
            amount=saving_box.amount,
        )