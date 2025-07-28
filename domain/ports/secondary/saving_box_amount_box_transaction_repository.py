from domain.entities.saving_box_amount_box_transaction import SavingBoxAmountBoxTransaction
from typing import Optional, List
from abc import ABC, abstractmethod

class ISavingBoxAmountBoxTransactionRepository:
    """Interfaz para el repositorio de SavingBoxAmountBoxTransaction"""

    @abstractmethod
    def save(self, saving_box_amount_box_transaction: SavingBoxAmountBoxTransaction) -> None:
        """Guarda una SavingBoxAmountBoxTransaction en la base de datos"""
        pass

    @abstractmethod
    def get_by_id(self, id: int) -> Optional[SavingBoxAmountBoxTransaction]:
        """Obtiene una SavingBoxAmountBoxTransaction por su id"""
        pass

    @abstractmethod
    def get_by_saving_box_id(self, saving_box_id: int) -> List[SavingBoxAmountBoxTransaction]:
        """Obtiene todas las SavingBoxAmountBoxTransaction por el id de la caja de ahorro"""
        pass

    @abstractmethod
    def get_by_amount_box_id(self, amount_box_id: int) -> List[SavingBoxAmountBoxTransaction]:
        """Obtiene todas las SavingBoxAmountBoxTransaction por el id de la caja de ahorro"""
        pass

    @abstractmethod
    def get_total_amount_by_saving_box_id(self, saving_box_id: int) -> Optional[SavingBoxAmountBoxTransaction]:
        """Metodo para obtener toda la cantidad de transacciones de una caja de ahorro"""
        pass

    @abstractmethod
    def get_total_amount_by_amount_box_id(self, amount_box_id: int) -> Optional[SavingBoxAmountBoxTransaction]:
        """Metodo para obtener toda la cantidad de transacciones de una caja"""
        pass

    @abstractmethod
    def save_transaction(self, saving_box_amount_box_transaction: SavingBoxAmountBoxTransaction) -> bool:
        """Metodo para guardar una transaccion de la caja de ahorro a la caja amount"""
        pass