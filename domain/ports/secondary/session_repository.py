from abc import ABC, abstractmethod
from typing import Optional
from domain.entities.session import Session

class ISessionRepository(ABC):
    """Puerto secundario para el repositorio de sesiones"""
    
    @abstractmethod
    def save(self, session: Session) -> bool:
        """Guarda una nueva sesión"""
        pass

    @abstractmethod
    def get_by_client_uuid(self, client_uuid: str) -> Optional[Session]:
        """Obtiene una sesión por client_uuid"""
        pass

    @abstractmethod
    def update_session_refresh_token(self, session: Session) -> bool:
        """Actualizar refresh token de una sesión, token_created_at y expires_at"""
        pass
    
    @abstractmethod
    def get_by_id(self, session_id: int) -> Optional[Session]:
        """Obtiene una sesión por ID"""
        pass
    
    @abstractmethod
    def get_by_refresh_token(self, refresh_token: str) -> Optional[Session]:
        """Obtiene una sesión por refresh token"""
        pass

    @abstractmethod
    def get_by_refresh_token_and_client_uuid(self, refresh_token: str, client_uuid: str) -> Optional[Session]:
        """Obtiene una sesión por refresh token y client_uuid"""
        pass
    
    @abstractmethod
    def get_by_client_uuid_and_user(self, client_uuid: str, user_id: int) -> Optional[Session]:
        """Obtiene una sesión por client_uuid y user_id"""
        pass
    
    @abstractmethod
    def update(self, session: Session) -> Session:
        """Actualiza una sesión existente"""
        pass
    
    @abstractmethod
    def delete(self, session_id: int) -> bool:
        """Elimina una sesión"""
        pass
    
    @abstractmethod
    def get_active_sessions_by_user(self, user_id: int) -> list[Session]:
        """Obtiene todas las sesiones activas de un usuario"""
        pass 