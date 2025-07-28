from domain.ports.secondary.box_clean_up_event_repository import IBoxCleanUpEventRepository
from domain.entities.box_clean_up_event import BoxCleanUpEvent
from infrastructure.persistence.models import BoxCleanUpEvent as BoxCleanUpEventModel
from typing import List

class BoxCleanUpEventRepository(IBoxCleanUpEventRepository):
    def register_box_clean_up_event(self, box_clean_up_event: BoxCleanUpEvent) -> BoxCleanUpEvent:
        # Registrar el evento de limpieza de caja
        box_clean_up_event_model = BoxCleanUpEventModel(
            user_id=box_clean_up_event.user_id,
            total_amount=box_clean_up_event.total_amount,
            created_at=box_clean_up_event.created_at,
            updated_at=box_clean_up_event.updated_at
        )

        box_clean_up_event_model.save()
        return box_clean_up_event_model.to_domain_entity()

    def get_all_box_clean_up_events_by_user_id(self, user_id: int) -> List[BoxCleanUpEvent]:
        box_clean_up_event_models = BoxCleanUpEventModel.objects.filter(user_id=user_id)
        return [box_clean_up_event_model.to_domain_entity() for box_clean_up_event_model in box_clean_up_event_models]