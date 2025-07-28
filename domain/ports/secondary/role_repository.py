from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.role import Role

class IRoleRepository(ABC):
    """Puerto secundario para el repositorio de roles"""
    
    @abstractmethod
    def get_by_id(self, role_id: int) -> Optional[Role]:
        """Obtiene un rol por su ID"""
        pass
    
    @abstractmethod
    def get_by_name(self, name: str) -> Optional[Role]:
        """Obtiene un rol por su nombre"""
        pass
    
    @abstractmethod
    def add(self, role: Role) -> None:
        """Agrega un rol al repositorio"""
        pass 