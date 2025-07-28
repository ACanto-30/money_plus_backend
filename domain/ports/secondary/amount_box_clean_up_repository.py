from abc import ABC, abstractmethod
from domain.entities.amount_box_clean_up import AmountBoxCleanUp
from typing import List

class IAmountBoxCleanUpRepository(ABC):
    @abstractmethod
    def register_amount_box_clean_up(self, amount_box_clean_up: AmountBoxCleanUp) -> AmountBoxCleanUp:
        pass