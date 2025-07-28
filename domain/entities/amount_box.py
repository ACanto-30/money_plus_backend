from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from domain.exceptions.implementations import InvalidDomainOperationException

@dataclass
class AmountBox:
    """Entidad AmountBox del dominio - Pura, sin dependencias"""

    id: Optional[int] = None
    name: str = ""
    amount: int = 0 # en centavos
    user_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def withdraw_amount(self, amount: int) -> int:
        """Metodo para retirar una cantidad de la caja"""
        if amount > self.amount:
            raise InvalidDomainOperationException("caja", amount, "La cantidad a retirar es mayor al saldo de la caja")
        print("dinero a retirar amount:", amount)
        print("dinero antes de retirar self.amount:", self.amount)
        self.amount -= amount
        print("dinero despues de retirar self.amount:", self.amount)
        return self.amount
    
    def clean(self) -> "AmountBox":
        """Limpia la caja de amount dejarla sin dinero, el update_at se actualiza solo si se hace la limpieza"""
        self.amount = 0
        return self