from domain.ports.secondary.box_clean_up_detail_repository import IBoxCleanUpDetailRepository
from domain.entities.box_clean_up_detail import BoxCleanUpDetail
from infrastructure.persistence.models import BoxCleanUpDetail as BoxCleanUpDetailModel

class BoxCleanUpDetailRepository(IBoxCleanUpDetailRepository):
    def register_box_clean_up_detail(self, box_clean_up_detail: BoxCleanUpDetail) -> BoxCleanUpDetail:
        box_clean_up_detail_model = BoxCleanUpDetailModel(
            box_id=box_clean_up_detail.box_id,
            amount=box_clean_up_detail.amount,
            box_cleanup_event_id=box_clean_up_detail.box_cleanup_event_id,
            created_at=box_clean_up_detail.created_at,
            updated_at=box_clean_up_detail.updated_at
        )
        box_clean_up_detail_model.save()
        return box_clean_up_detail_model.to_domain_entity()
        
