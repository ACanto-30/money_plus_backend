from abc import ABC, abstractmethod
from domain.entities.box_clean_up_detail import BoxCleanUpDetail

class IBoxCleanUpDetailService(ABC):
    @abstractmethod
    def register_box_clean_up_detail(self, box_clean_up_detail: BoxCleanUpDetail) -> BoxCleanUpDetail:
        pass

