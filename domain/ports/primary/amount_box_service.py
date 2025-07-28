from abc import ABC, abstractmethod
from domain.entities.amount_box import AmountBox

class IAmountBoxService(ABC):
    @abstractmethod
    def get_amount_box_by_id(self, amount_box_id: int) -> AmountBox:
        pass

    @abstractmethod
    def get_amount_box_by_user_id(self, user_id: int) -> AmountBox:
        pass

    @abstractmethod
    def make_amount_box_transaction(self, amount_box: AmountBox) -> bool:
        pass

    @abstractmethod
    def create_amount_box(self, amount_box: AmountBox) -> bool:
        pass

    @abstractmethod
    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        pass