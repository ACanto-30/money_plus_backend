from abc import ABC, abstractmethod
from domain.entities.box_transaction import BoxTransaction

class IBoxTransactionRepository(ABC):
    
    @abstractmethod
    def make_box_transaction(self, box_transaction: BoxTransaction) -> BoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        pass