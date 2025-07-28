from abc import ABC, abstractmethod
from domain.entities.box import Box
from typing import List

class IBoxRepository(ABC):

    @abstractmethod
    def save_box(self, user_id: int, name: str) -> Box:
        """Metodo para guardar una caja"""
        pass

    @abstractmethod
    def get_box_active_by_amount_box_id(self, amount_box_id: int) -> Box:
        """Metodo para obtener la caja por el id de la caja de dinero y que este activa"""
    
    @abstractmethod
    def make_box_active_transaction(self, box: Box) -> Box:
        """Metodo para hacer una transaccion en la caja"""
        pass

    @abstractmethod
    def get_box_active_by_id(self, box_id: int) -> Box:
        """Metodo para obtener la caja por el id y que este activa"""
        pass

    @abstractmethod
    def get_box_active_by_user_id(self, user_id: int) -> Box:
        """Metodo para obtener la caja por el id del usuario y que este activa"""
        pass

    @abstractmethod
    def get_all_boxes_active_by_user_id(self, user_id: int) -> List[Box]:
        """Metodo para obtener todas las cajas activas por el id del usuario"""
        pass

    @abstractmethod
    def make_box_deactive_box(self, box_id: int, user_id: int) -> Box:
        """Metodo para desactivar una caja"""
        pass
    
    @abstractmethod
    def is_owner_box(self, box_id: int, user_id: int) -> bool:
        """Metodo para verificar si el usuario es el propietario de la caja"""
        pass

    @abstractmethod
    def update_box_name(self, box_id: int, name: str) -> Box:
        """Metodo para actualizar el nombre de la caja"""
        pass