from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from domain.exceptions.implementations import InvalidDomainOperationException

@dataclass
class SavingBox:
    """Entidad SavingBox del dominio - Pura, sin dependencias"""
    id: Optional[int] = None
    amount: int = 0 # en centavos
    user_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def withdraw_amount(self, amount: int) -> int:
        """Metodo para retirar una cantidad de la caja de ahorro"""
        if amount > self.amount:
            raise InvalidDomainOperationException("transaccion", amount, "La cantidad a retirar es mayor al saldo de la caja")
        self.amount -= amount
        return self.amount

    