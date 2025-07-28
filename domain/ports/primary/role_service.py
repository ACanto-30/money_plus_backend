from abc import ABC, abstractmethod
from domain.entities.role import Role

class IRoleService(ABC):
    """Puerto primario para el servicio de roles"""
    @abstractmethod
    def get_role_by_id(self, role_id: int) -> Role:
        """Obtiene un rol por ID"""
        pass