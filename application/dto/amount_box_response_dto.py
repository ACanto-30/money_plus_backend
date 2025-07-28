from pydantic import BaseModel, Field
from domain.entities.amount_box import AmountBox

class AmountBoxResponseDTO(BaseModel):
    id: int = Field(..., description="ID de la caja de ahorro")
    amount: int = Field(..., description="Cantidad total de la caja de ahorro")
    
    @classmethod
    def from_entity(cls, amount_box: AmountBox):
        return cls(
            id=amount_box.id,
            amount=amount_box.amount,
        )