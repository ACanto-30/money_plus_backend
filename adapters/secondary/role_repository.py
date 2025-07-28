from typing import Optional
from domain.entities.role import Role as RoleEntity
from domain.ports.secondary.role_repository import IRoleRepository
from infrastructure.persistence.models import Role

class RoleRepository(IRoleRepository):
    """Implementación del repositorio de roles"""
    
    def get_by_id(self, role_id: int) -> Optional[RoleEntity]:
        """Obtiene un rol por su ID"""
        try:
            role_model = Role.objects.get(id=role_id)
            return role_model.to_domain_entity()
        except Role.DoesNotExist:
            return None
    
    def get_by_name(self, name: str) -> Optional[RoleEntity]:
        """Obtiene un rol por su nombre"""
        try:
            role_model = Role.objects.get(name=name)
            return role_model.to_domain_entity()
        except Role.DoesNotExist:
            return None
    
    def add(self, role: RoleEntity) -> None:
        """Agrega un rol al repositorio"""
        role_model = Role.from_domain_entity(role)
        role_model.save()
        # Actualizar el ID en la entidad
        role.id = role_model.id