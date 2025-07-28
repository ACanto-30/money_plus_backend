from abc import ABC, abstractmethod
from domain.entities.box_clean_up_event import BoxCleanUpEvent
from typing import List

class IBoxCleanUpEventService(ABC):
    
    @abstractmethod
    def register_box_clean_up_event(self, box_clean_up_event: BoxCleanUpEvent) -> BoxCleanUpEvent:
        pass

    @abstractmethod
    def get_all_box_clean_up_events_by_user_id(self, user_id: int) -> List[BoxCleanUpEvent]:
        pass
    
    
