from abc import ABC, abstractmethod
from domain.entities.user import User

class IUserService(ABC):
    """Puerto primario para el servicio de usuarios"""
    @abstractmethod
    def get_user_by_id(self, user_id: int) -> User:
        """Obtiene un usuario por ID"""
        pass

    @abstractmethod
    def get_user_by_email(self, email: str) -> User:
        """Obtiene un usuario por email"""
        pass