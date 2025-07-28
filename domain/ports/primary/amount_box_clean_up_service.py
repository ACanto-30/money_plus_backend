from abc import ABC, abstractmethod
from domain.entities.amount_box_clean_up import AmountBoxCleanUp

class IAmountBoxCleanUpService(ABC):
    @abstractmethod
    def register_amount_box_clean_up(self, amount_box_clean_up: AmountBoxCleanUp) -> AmountBoxCleanUp:
        pass
