from abc import ABC, abstractmethod
from typing import List
from domain.entities.box import Box
from domain.entities.box_clean_up_event import BoxCleanUpEvent

class ICleanBoxService(ABC):
    """Interfaz para el servicio de limpieza de cajas"""

    @abstractmethod
    def clean_box(self, box_id: int) -> int:
        """Limpia una caja"""
        pass

    @abstractmethod
    def clean_amount_box(self, amount_box_id: int) -> int:
        """Limpia una caja de amount"""
        pass

    @abstractmethod
    def clean_all_boxes_by_user_id(self, user_id: int) -> bool:
        """Limpia todas las cajas de un usuario"""
        pass

    @abstractmethod
    def get_all_boxes_by_user_id(self, user_id: int) -> List[Box]:
        """Obtiene todas las cajas de un usuario"""
        pass
    
    @abstractmethod
    def get_all_box_clean_up_events_by_user_id(self, user_id: int) -> List[BoxCleanUpEvent]:
        """Obtiene todas las limpiezas de cajas de un usuario"""
        pass

