from .base_dto import BaseDTO
from pydantic import Field

class TransferDTO(BaseDTO):
    """DTO para transacciones"""
    to_box_id: int = Field(..., description="ID de la caja destino")
    amount: int = Field(..., description="Cantidad de la transaccion", gt=0)
    transaction_type_id: int = Field(..., description="ID del tipo de transaccion")