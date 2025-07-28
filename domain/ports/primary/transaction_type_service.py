from abc import ABC, abstractmethod
from domain.entities.transaction_type import TransactionType

class ITransactionTypeService(ABC):
    @abstractmethod
    def get_transaction_type_by_id(self, transaction_type_id: int) -> TransactionType:
        pass