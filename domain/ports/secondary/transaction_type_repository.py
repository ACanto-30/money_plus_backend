from abc import ABC, abstractmethod
from typing import List
from domain.entities.transaction_type import TransactionType
from enum import Enum

class ITransactionTypeRepository(ABC):
    @abstractmethod
    def get_transaction_type_by_id(self, transaction_type_id: int) -> TransactionType:
        """Metodo para obtener el tipo de transaccion por el id"""
        pass

    @abstractmethod
    def get_all_transaction_types(self) -> List[TransactionType]:
        """Metodo para obtener todos los tipos de transaccion"""
        pass

class TransactionTypeEnum(Enum):
    """Enum para los tipos de transaccion"""
    DEPOSIT = 1
    WITHDRAW = 2
    CLEAN_BOX = 3
    REPAYMENT = 4
