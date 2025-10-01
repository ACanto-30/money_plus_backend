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
    
    def add(self, role: RoleEntity) -> RoleEntity:
        """Agrega un rol al repositorio y retorna la entidad con ID asignado"""
        role_model = Role.from_domain_entity(role)
        role_model.save()
        
        # Actualizar la entidad con los datos de la base de datos
        role.id = role_model.id
        role.created_at = role_model.created_at
        role.updated_at = role_model.updated_at
        
        return role