from pydantic import Field
from .base_dto import BaseDTO

class TransactionDTO(BaseDTO):
    """DTO para transacciones"""
    amount: int = Field(..., description="Cantidad de la transaccion", gt=0)
    transaction_type_id: int = Field(..., description="ID del tipo de transaccion")