from abc import ABC, abstractmethod
from domain.entities.amount_box_transaction import AmountBoxTransaction
from typing import List

class IAmountBoxTransactionRepository(ABC):
    @abstractmethod
    def get_all_amount_box_transactions_by_amount_box_id(self, amount_box_id: int) -> List[AmountBoxTransaction]:
        """Metodo para obtener todas las transacciones de la caja por el id de la caja"""
        pass
    
    @abstractmethod
    def make_amount_box_transaction(self, amount_box_transaction: AmountBoxTransaction) -> AmountBoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        pass
    
    @abstractmethod
    def get_all_amount_box_transactions_by_user_id(self, user_id: int) -> List[AmountBoxTransaction]:
        """Metodo para obtener todas las transacciones de la caja por el id del usuario"""
        pass
    
    @abstractmethod
    def get_all_amount_box_transactions_by_amount_box_id_and_user_id(self, amount_box_id: int, user_id: int) -> List[AmountBoxTransaction]:
        """Metodo para obtener todas las transacciones de la caja por el id de la caja y el id del usuario"""
        pass
    