from abc import ABC, abstractmethod
from domain.entities.saving_box import SavingBox
from typing import List

class ISavingBoxRepository(ABC):
    @abstractmethod
    def get_saving_box_by_user_id(self, user_id: int) -> SavingBox:
        """Metodo para obtener la caja de ahorro por el id del usuario"""
        pass

    @abstractmethod
    def get_saving_box_by_id(self, saving_box_id: int) -> SavingBox:
        """Metodo para obtener la caja de ahorro por el id"""
        pass

    @abstractmethod
    def get_all_saving_boxes_by_user_id(self, user_id: int) -> List[SavingBox]:
        """Metodo para obtener todas las cajas de ahorro por el id del usuario"""
        pass

    @abstractmethod
    def create_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para crear una caja de ahorro"""
        pass
    
    @abstractmethod
    def update_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para actualizar una caja de ahorro"""
        pass
    
    @abstractmethod
    def delete_saving_box(self, saving_box_id: int) -> bool:
        """Metodo para eliminar una caja de ahorro"""
        pass

    @abstractmethod
    def withdraw_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para retirar dinero de una caja de ahorro (unica por usuario), el dinero ya contado o descontado del service
        solo listo para actualizar el estado de la caja de ahorro"""
        pass
    
    @abstractmethod
    def deposit_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para depositar dinero en una caja de ahorro (unica por usuario), el dinero ya contado o descontado del service
        solo listo para actualizar el estado de la caja de ahorro"""
        pass
    
