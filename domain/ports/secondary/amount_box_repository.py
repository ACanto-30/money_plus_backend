from abc import ABC, abstractmethod
from domain.entities.amount_box import AmountBox
from typing import List

class IAmountBoxRepository(ABC):
    @abstractmethod
    def get_amount_box_by_user_id(self, user_id: int) -> AmountBox:
        """Metodo para obtener la cantidad de la caja por el id del usuario"""
        pass
    
    @abstractmethod
    def get_all_amount_boxes_by_user_id(self, user_id: int) -> List[AmountBox]:
        """Metodo para obtener todas las cantidades de la caja por el id del usuario"""
        pass

    @abstractmethod
    def create_amount_box(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para crear una nueva caja de dinero"""
        pass

    @abstractmethod
    def deposit_amount_box(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para depositar una cantidad en la caja"""
        pass
    
    @abstractmethod
    def make_amount_box_transaction(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para hacer una transaccion en la caja"""
        pass