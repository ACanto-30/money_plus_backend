from domain.ports.primary.role_service import IRoleService
from domain.ports.secondary.role_repository import IRoleRepository
from infrastructure.configuration.container import Container
from domain.entities.role import Role
from domain.exceptions.implementations import InvalidDomainOperationException

class RoleService(IRoleService):
    def __init__(self):
        self._role_repository = Container.resolve(IRoleRepository)

    def get_role_by_id(self, role_id: int) -> Role:
        """Obtiene un rol por ID"""
        role = self._role_repository.get_by_id(role_id)
        if not role:
            raise InvalidDomainOperationException("Role", role_id, "El rol no existe")
        return role