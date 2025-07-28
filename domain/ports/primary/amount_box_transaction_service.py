from abc import ABC, abstractmethod
from domain.entities.amount_box_transaction import AmountBoxTransaction

class IAmountBoxTransactionService(ABC):
    @abstractmethod
    def make_amount_box_transaction(self, amount_box_transaction: AmountBoxTransaction) -> bool:
        """Metodo para hacer una transaccion en la caja"""
        pass

    @abstractmethod
    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        """Metodo para obtener el monto de la caja de ahorro"""
        pass