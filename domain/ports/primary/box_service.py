from abc import ABC, abstractmethod
from domain.entities.box import Box
from typing import List

class IBoxService(ABC):
    @abstractmethod
    def get_box_by_id(self, box_id: int) -> Box:
        pass

    @abstractmethod
    def get_box_by_user_id(self, user_id: int) -> Box:
        pass

    @abstractmethod
    def get_all_boxes_by_user_id(self, user_id: int) -> List[Box]:
        pass

    @abstractmethod
    def make_box_transaction(self, box: Box) -> Box:
        pass

    @abstractmethod
    def deactive_box(self, box_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def create_box(self, box: Box) -> Box:
        pass

    @abstractmethod
    def save_box(self, user_id: int, name: str) -> Box:
        pass

    @abstractmethod
    def is_owner_box(self, box_id: int, user_id: int) -> bool:
        pass

    @abstractmethod
    def update_box_name(self, box_id: int, name: str) -> Box:
        pass
