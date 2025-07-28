from domain.entities.saving_box_box_transaction import SavingBoxBoxTransaction
from typing import Optional, List
from abc import ABC, abstractmethod

class ISavingBoxBoxTransactionRepository(ABC):
    """Interfaz para el repositorio de SavingBoxBoxTransaction"""

    @abstractmethod
    def save(self, saving_box_box_transaction: SavingBoxBoxTransaction) -> SavingBoxBoxTransaction:
        """Guarda una SavingBoxBoxTransaction en la base de datos"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[SavingBoxBoxTransaction]:
        """Obtiene una SavingBoxBoxTransaction por su id"""
        pass

    