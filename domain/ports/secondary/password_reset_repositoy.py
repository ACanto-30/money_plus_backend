from abc import ABC, abstractmethod
from typing import Optional, List
from domain.entities.password_reset import PasswordReset
from datetime import datetime
class IPasswordResetRepository(ABC):
    """Puerto secundario para el repositorio de contraseñas de reseteo"""

    @abstractmethod
    def get_code(self, code: int) -> Optional[PasswordReset]:
        """Obtiene un código de reseteo por su código si existe y no ha expirado"""
        pass

    @abstractmethod
    def get_code_by_user_id(self, user_id: int) -> Optional[PasswordReset]:
        """Obtiene un código de reseteo por el id del usuario y si este no esta expirado"""
        pass

    @abstractmethod
    def get_expired_codes(self) -> List[PasswordReset]:
        """Obtiene los códigos de reseteo que han expirado"""
        pass

    @abstractmethod
    def invalidate_code(self, code: int) -> bool:
        """Invalida un código de reseteo en la base de datos"""
        pass

    @abstractmethod
    def save_code(self, code: int, user_id: int, expires_at: datetime) -> bool:
        """Guarda un código de reseteo en la base de datos"""
        pass

    @abstractmethod
    def update_code(self, new_code: int, user_id: int) -> bool:
        """Actualiza un código de reseteo en la base de datos"""