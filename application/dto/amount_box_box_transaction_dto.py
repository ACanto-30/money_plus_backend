from pydantic import Field
from .base_dto import BaseDTO

class AmountBoxBoxTransactionDTO(BaseDTO):
    """DTO para transaccion de caja"""
    
    # El amount tiene que ser mayor a 0
    from_box_id: int = Field(..., description="Id de la caja de origen")
    amount: int = Field(..., description="Cantidad de la transaccion", gt=0)
    transaction_type_id: int = Field(..., description="Tipo de transaccion")

