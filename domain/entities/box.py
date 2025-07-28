from dataclasses import dataclass
from typing import Optional
from datetime import datetime, timezone
from domain.exceptions.implementations import InvalidDomainOperationException

@dataclass
class Box:
    """Entidad Box del dominio - Pura, sin dependencias"""
    
    id: Optional[int] = None
    name: str = ""
    is_active: bool = True
    amount: int = 0 # en centavos
    user_id: int = 0
    created_at: datetime = datetime.now(timezone.utc)
    updated_at: datetime = datetime.now(timezone.utc)

    def __post_init__(self):
        """Validaciones básicas de dominio"""
        if not self.name or self.name.strip() == "":
            raise ValueError("Box name cannot be empty.")
        
        if self.amount < 0:
            raise ValueError("Box amount cannot be negative.")

    def clean(self) -> "Box":
        """Limpia la caja dejarla sin dinero, el update_at se actualiza solo si se hace la limpieza"""
        self.amount = 0
        return self

    def withdraw_amount(self, amount: int) -> int:
        """Metodo para retirar una cantidad de la caja"""
        if amount > self.amount:
            raise InvalidDomainOperationException("caja", amount, "La cantidad a retirar es mayor al saldo de la caja")
        self.amount -= amount
        return self.amount
