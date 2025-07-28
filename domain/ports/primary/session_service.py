from abc import ABC, abstractmethod
from domain.commands.session_command import SessionCommand
from domain.entities.session import Session

class ISessionService(ABC):
    """Puerto primario para el servicio de sesiones"""
    @abstractmethod
    def create_session(self, session_command: SessionCommand) -> bool:
        """Crea una sesión para un usuario"""
        pass
    
    @abstractmethod
    def get_session_by_client_uuid(self, client_uuid: str) -> Session:
        """Obtiene una sesión por client_uuid"""
        pass