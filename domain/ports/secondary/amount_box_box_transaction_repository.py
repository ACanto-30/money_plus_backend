from abc import ABC, abstractmethod
from domain.entities.amount_box_box_transaction import AmountBoxBoxTransaction

class IAmountBoxBoxTransactionRepository(ABC):
    @abstractmethod
    def make_amount_box_box_transaction(self, amount_box_box_transaction: AmountBoxBoxTransaction) -> AmountBoxBoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        pass
    