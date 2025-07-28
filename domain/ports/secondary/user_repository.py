from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.user import User

class IUserRepository(ABC):
    """Puerto secundario para el repositorio de usuarios"""
    
    @abstractmethod
    def save(self, user: User) -> int:
        """Agrega un usuario al repositorio"""
        pass
    
    @abstractmethod
    def get_by_role_id(self, role_id: int) -> Optional[User]:
        """Obtiene un usuario por su role_id"""
        pass

    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        """Obtiene un usuario por su email"""
        pass

    @abstractmethod
    def get_by_id(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario por su id"""
        pass
    
    @abstractmethod
    def update_password(self, user_id: int, new_password: str) -> bool:
        """Actualiza la contraseña de un usuario"""
        pass
    
    @abstractmethod
    def get_user_with_boxes(self, user_id: int) -> Optional[User]:
        """Obtiene un usuario con sus cajas relacionadas"""
        pass
    
    @abstractmethod
    def get_user_and_boxes_data(self, user_id: int) -> Optional[dict]:
        """Obtiene datos de usuario y boxes en formato diccionario"""
        pass
    