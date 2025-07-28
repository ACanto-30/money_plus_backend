from domain.ports.secondary.password_reset_repositoy import IPasswordResetRepository
from domain.entities.password_reset import PasswordReset
from typing import Optional, List
from infrastructure.persistence.models import PasswordReset as PasswordResetModel
from datetime import datetime
from django.utils import timezone

class PasswordResetRepository(IPasswordResetRepository):
    """Implementación del repositorio de contraseñas de reseteo"""

    def get_code(self, code: int) -> Optional[PasswordReset]:
        """Obtiene un código de reseteo por su código si existe y no ha expirado y no esta usado"""
        try:
            password_reset_model = PasswordResetModel.objects.get(code=code, expires_at__gt=timezone.now(), is_used=False)
            return password_reset_model.to_domain_entity()
        except PasswordResetModel.DoesNotExist:
            return None

    def get_code_by_user_id(self, user_id: int) -> Optional[PasswordReset]:
        """Obtiene un código de reseteo por el id del usuario y si este no esta expirado"""
        try:
            password_reset_model = PasswordResetModel.objects.get(user_id=user_id, expires_at__gt=timezone.now())
            return password_reset_model.to_domain_entity()
        except PasswordResetModel.DoesNotExist:
            return None
    def get_code_by_user_id_and_not_expired(self, user_id: int) -> Optional[PasswordReset]:
        """Obtiene un código de reseteo por el id del usuario que no esté expirado y no haya sido usado"""
        try:
            password_reset_model = PasswordResetModel.objects.get(
                user_id=user_id, 
                expires_at__gt=timezone.now(),
                is_used=False
            )
            return password_reset_model.to_domain_entity()
        except PasswordResetModel.DoesNotExist:
            return None

    def get_expired_codes(self) -> list[PasswordReset]:
        """Obtiene todos los códigos de reseteo que han expirado y no han sido usados"""
        try:
            # Usar timezone.now() para comparación correcta con USE_TZ=True
            current_time = timezone.now()
            print(f"Buscando códigos expirados antes de: {current_time}")
            
            expired_models = PasswordResetModel.objects.filter(
                expires_at__lt=current_time,
                is_used=False
            )
            
            print(f"Consulta SQL: {expired_models.query}")
            print(f"Modelos encontrados: {expired_models.count()}")
            
            return [model.to_domain_entity() for model in expired_models]
        except Exception as e:
            print(f"Error en get_expired_codes: {str(e)}")
            return []

    def invalidate_code(self, code: int) -> bool:
        """Invalida un código de reseteo en la base de datos"""
        password_reset_model = PasswordResetModel.objects.get(code=code)
        password_reset_model.is_used = True
        password_reset_model.save()
        return True

    def save_code(self, code: int, user_id: int, expires_at: datetime) -> bool:
        """Guarda un código de reseteo en la base de datos"""
        password_reset_model = PasswordResetModel.objects.create(
            code=code, 
            user_id=user_id, 
            expires_at=expires_at,
            created_at=timezone.now(),
            is_used=False
        )
        return True

    def update_code(self, new_code: int, user_id: int) -> bool:
        """Actualiza un código de reseteo en la base de datos"""
        password_reset_model = PasswordResetModel.objects.get(user_id=user_id)
        password_reset_model.code = new_code
        password_reset_model.save()
        return True
