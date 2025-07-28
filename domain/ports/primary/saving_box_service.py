from abc import ABC, abstractmethod
from domain.entities.saving_box import SavingBox

class ISavingBoxService(ABC):
    @abstractmethod
    def make_saving_box_transaction(self, saving_box: SavingBox) -> bool:
        """Metodo para hacer una transaccion de la caja de ahorro"""
        pass

    @abstractmethod
    def create_saving_box(self, saving_box: SavingBox) -> bool:
        """Metodo para crear una caja de ahorro"""
        pass

    @abstractmethod
    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        """Metodo para obtener el monto de la caja de ahorro"""
        pass