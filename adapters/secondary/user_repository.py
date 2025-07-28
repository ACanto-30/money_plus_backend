from typing import Optional
from django.db import transaction
from domain.entities.user import User as UserEntity
from domain.ports.secondary.user_repository import IUserRepository
from infrastructure.persistence.models import User, Role

class UserRepository(IUserRepository):
    """Implementación del repositorio de usuarios"""
    
    def save(self, user: UserEntity) -> int:
        """Agrega un usuario al repositorio"""
        user_model = User.from_domain_entity(user)
        user_model.save()
        return user_model.id
    
    def get_by_role_id(self, role_id: int) -> Optional[UserEntity]:
        """Obtiene un usuario por su role_id"""
        try:
            user_model = User.objects.select_related('role').get(role_id=role_id)
            return user_model.to_domain_entity()
        except User.DoesNotExist:
            return None
        
    def get_by_email(self, email: str) -> Optional[UserEntity]:
        """Obtiene un usuario por su email sin role"""
        try:
            user_model = User.objects.get(email=email)
            return user_model.to_domain_entity()
        except User.DoesNotExist:
            return None

    def get_by_id(self, user_id: int) -> Optional[UserEntity]:
        """Obtiene un usuario por su id"""
        try:
            user_model = User.objects.get(id=user_id)
            return user_model.to_domain_entity()
        except User.DoesNotExist:
            return None
    
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Actualiza la contraseña de un usuario"""
        user_model = User.objects.get(id=user_id)
        user_model.password = new_password
        user_model.save()
        return True
    
    def get_user_with_boxes(self, user_id: int) -> Optional[UserEntity]:
        """Obtiene un usuario con sus cajas relacionadas"""
        try:
            user_model = User.get_user_with_boxes_optimized(user_id)
            if user_model:
                return user_model.to_domain_entity_with_boxes()
            return None
        except User.DoesNotExist:
            return None
    
    def get_user_and_boxes_data(self, user_id: int) -> Optional[dict]:
        """Obtiene datos de usuario y boxes en una sola consulta optimizada"""
        from django.db.models import Prefetch
        from infrastructure.persistence.models import Box
        
        try:
            # Consulta optimizada: una sola consulta con prefetch
            user_model = User.objects.select_related('role').prefetch_related(
                Prefetch(
                    'amount_boxes__boxes',
                    queryset=Box.objects.only('id', 'name', 'created_at')
                )
            ).get(id=user_id)
            
            # Construir respuesta directamente
            boxes_data = []
            for amount_box in user_model.amount_boxes.all():
                for box in amount_box.boxes.all():
                    boxes_data.append({
                        'box_id': box.id,
                        'name': box.name,
                        'created_at': box.created_at
                    })
            
            return {
                'user_id': user_model.id,
                'username': user_model.username,
                'created_at': user_model.created_at,
                'boxes': boxes_data
            }
            
        except User.DoesNotExist:
            return None