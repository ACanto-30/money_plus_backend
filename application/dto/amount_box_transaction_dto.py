from pydantic import Field
from .base_dto import BaseDTO

class AmountBoxTransactionDTO(BaseDTO):
    """DTO para transaccion de caja"""
    
    # El amount tiene que ser mayor a 0
    amount: int = Field(..., description="Cantidad de la transaccion", gt=0)
    transaction_type_id: int = Field(..., description="Tipo de transaccion")

