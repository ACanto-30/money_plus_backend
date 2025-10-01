from domain.ports.primary.role_service import IRoleService
from domain.ports.secondary.role_repository import IRoleRepository
from infrastructure.configuration.container import Container
from domain.entities.role import Role
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.commands.role_add_command import RoleAddCommand

class RoleService(IRoleService):
    def __init__(self):
        self._role_repository = Container.resolve(IRoleRepository)

    def get_role_by_id(self, role_id: int) -> Role:
        """Obtiene un rol por ID"""
        role = self._role_repository.get_by_id(role_id)
        if not role:
            raise InvalidDomainOperationException("Role", role_id, "El rol no existe")
        return role
    
    def add_role(self, command: RoleAddCommand) -> Role:
        """Crea un rol"""
        # Convertir el comando a una entidad de dominio
        role_entity = Role(
            name=command.name,
            description=command.description
        )
        
        # Agregar al repositorio
        self._role_repository.add(role_entity)
        
        # Retornar la entidad con el ID asignado por la base de datos
        return role_entity