from domain.ports.primary.box_clean_up_event_service import IBoxCleanUpEventService
from domain.entities.box_clean_up_event import BoxCleanUpEvent
from domain.ports.secondary.box_clean_up_event_repository import IBoxCleanUpEventRepository
from infrastructure.configuration.container import Container
from typing import List

class BoxCleanUpEventService(IBoxCleanUpEventService):
    def __init__(self):
        self.box_clean_up_event_repository = Container.resolve(IBoxCleanUpEventRepository)

    def register_box_clean_up_event(self, box_clean_up_event: BoxCleanUpEvent) -> BoxCleanUpEvent:
        return self.box_clean_up_event_repository.register_box_clean_up_event(box_clean_up_event)

    def get_all_box_clean_up_events_by_user_id(self, user_id: int) -> List[BoxCleanUpEvent]:
        return self.box_clean_up_event_repository.get_all_box_clean_up_events_by_user_id(user_id)