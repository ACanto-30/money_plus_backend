from abc import ABC, abstractmethod
from domain.entities.role import Role
from domain.commands.role_add_command import RoleAddCommand

class IRoleService(ABC):
    """Puerto primario para el servicio de roles"""
    @abstractmethod
    def get_role_by_id(self, role_id: int) -> Role:
        """Obtiene un rol por ID"""
        pass
    
    @abstractmethod
    def add_role(self, command: RoleAddCommand) -> Role:
        """Crea un rol"""
        pass