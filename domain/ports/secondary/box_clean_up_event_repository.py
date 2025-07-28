from abc import ABC, abstractmethod
from domain.entities.box_clean_up_event import BoxCleanUpEvent

class IBoxCleanUpEventRepository(ABC):
    @abstractmethod
    def register_box_clean_up_event(self, box_clean_up_event: BoxCleanUpEvent) -> BoxCleanUpEvent:
        pass