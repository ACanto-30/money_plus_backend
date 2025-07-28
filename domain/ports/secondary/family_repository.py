from abc import ABC, abstractmethod
from domain.entities.family import Family
from typing import List

class IFamilyRepository(ABC):
    @abstractmethod
    def get_family_by_id(self, family_id: int) -> Family:
        """Metodo para obtener la familia por el id"""
        pass

    @abstractmethod
    def get_all_families(self) -> List[Family]:
        """Metodo para obtener todas las familias"""
        pass

    @abstractmethod
    def create_family(self, family: Family) -> Family:
        """Metodo para crear una familia"""
        pass

    @abstractmethod
    def update_family(self, family: Family) -> Family:
        """Metodo para actualizar una familia"""
        pass
    
    @abstractmethod
    def delete_family(self, family_id: int) -> bool:
        """Metodo para eliminar una familia"""
        pass
    
    @abstractmethod
    def get_family_by_family_code(self, family_code: str) -> Family:
        """Metodo para obtener una familia por el codigo de la familia"""
        pass
    
    