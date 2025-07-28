from domain.ports.primary.box_clean_up_detail_service import IBoxCleanUpDetailService
from domain.entities.box_clean_up_detail import BoxCleanUpDetail
from domain.ports.secondary.box_clean_up_detail_repository import IBoxCleanUpDetailRepository
from infrastructure.configuration.container import Container

class BoxCleanUpDetailService(IBoxCleanUpDetailService):
    def __init__(self):
        self.box_clean_up_detail_repository = Container.resolve(IBoxCleanUpDetailRepository)

    def register_box_clean_up_detail(self, box_clean_up_detail: BoxCleanUpDetail) -> BoxCleanUpDetail:
        return self.box_clean_up_detail_repository.register_box_clean_up_detail(box_clean_up_detail)