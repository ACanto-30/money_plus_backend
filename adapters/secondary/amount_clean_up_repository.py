from domain.ports.secondary.amount_box_clean_up_repository import IAmountBoxCleanUpRepository
from domain.entities.amount_box_clean_up import AmountBoxCleanUp
from infrastructure.persistence.models import AmountBoxCleanUp as AmountBoxCleanUpModel

class AmountBoxCleanUpRepository(IAmountBoxCleanUpRepository):
    def register_amount_box_clean_up(self, amount_box_clean_up: AmountBoxCleanUp) -> AmountBoxCleanUp:
        amount_box_clean_up_model = AmountBoxCleanUpModel(
            amount_box_id=amount_box_clean_up.amount_box_id,
            total_amount=amount_box_clean_up.total_amount,
            box_cleanup_event_id=amount_box_clean_up.box_cleanup_event_id
        )
        amount_box_clean_up_model.save()
        return amount_box_clean_up_model.to_domain_entity()

