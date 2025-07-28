from domain.ports.primary.box_service import IBoxService
from domain.entities.box import Box
from infrastructure.configuration.container import Container
from domain.ports.secondary.box_repository import IBoxRepository
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from typing import List

class BoxService(IBoxService):
    def __init__(self):
        self._box_repository = Container.resolve(IBoxRepository)

    def get_box_by_id(self, box_id: int) -> Box:
        box = self._box_repository.get_box_active_by_id(box_id)
        if not box:
            raise InvalidDomainOperationException("caja", box_id, "La caja no existe")
        return box

    def get_box_by_user_id(self, user_id: int) -> Box:
        box = self._box_repository.get_box_active_by_user_id(user_id)
        if not box:
            raise InvalidDomainOperationException("caja", user_id, "La caja no existe")
        return box

    def make_box_transaction(self, box: Box) -> bool:
        self._box_repository.make_box_active_transaction(box)
        return True

    def deactive_box(self, box_id: int, user_id: int) -> bool:
        self._box_repository.make_box_deactive_box(box_id, user_id)
        return True

    def save_box(self, user_id: int, name: str) -> Box:
        return self._box_repository.save_box(user_id, name)

    def create_box(self, box: Box) -> Box:
        self._box_repository.make_box_active_transaction(box)
        return box
    
    def get_all_boxes_by_user_id(self, user_id: int) -> List[Box]:
        return self._box_repository.get_all_boxes_active_by_user_id(user_id)
    
    def is_owner_box(self, box_id: int, user_id: int) -> bool:
        is_owner = self._box_repository.is_owner_box(box_id, user_id)
        if not is_owner:
            raise ForbiddenDomainOperationException.box_not_owner(box_id, user_id)
        return True

    def get_all_boxes_active_by_user_id(self, user_id: int) -> List[Box]:
        return self._box_repository.get_all_boxes_active_by_user_id(user_id)
    
    def update_box_name(self, box_id: int, name: str) -> Box:
        return self._box_repository.update_box_name(box_id, name)

    