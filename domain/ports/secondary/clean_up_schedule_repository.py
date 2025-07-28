from abc import ABC, abstractmethod
from domain.entities.clean_up_schedule import CleanUpSchedule
from typing import List

class ICleanUpScheduleRepository(ABC):
    
    @abstractmethod
    def get_clean_up_schedule_by_user_id(self, user_id: int) -> CleanUpSchedule:
        """Metodo para obtener la programación de limpieza por el id del usuario"""
        pass
    