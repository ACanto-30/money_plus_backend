from domain.ports.primary.amount_box_clean_up_service import IAmountBoxCleanUpService
from domain.entities.amount_box_clean_up import AmountBoxCleanUp
from domain.ports.secondary.amount_box_clean_up_repository import IAmountBoxCleanUpRepository
from infrastructure.configuration.container import Container

class AmountBoxCleanUpService(IAmountBoxCleanUpService):
    def __init__(self):
        self.amount_box_clean_up_repository = Container.resolve(IAmountBoxCleanUpRepository)

    def register_amount_box_clean_up(self, amount_box_clean_up: AmountBoxCleanUp) -> AmountBoxCleanUp:
        return self.amount_box_clean_up_repository.register_amount_box_clean_up(amount_box_clean_up)