from domain.ports.primary.session_service import ISessionService

from domain.ports.secondary.session_repository import ISessionRepository
from infrastructure.configuration.container import Container
from domain.entities.session import Session
from domain.commands.session_command import SessionCommand
from domain.exceptions.implementations import InvalidDomainOperationException

class SessionService(ISessionService):
    """Servicio de aplicación para sesiones"""
    def __init__(self):
        self._session_repository = Container.resolve(ISessionRepository)

    def create_session(self, session_command: SessionCommand) -> bool:
        """Crea una sesión para un usuario"""
        # Crear la sesión
        session = Session(
            user_id=session_command.user_id,
            refresh_token=session_command.refresh_token,
            client_uuid=session_command.client_uuid,
            token_created_at=session_command.token_created_at,
            expires_at=session_command.expires_at,
            is_active=True
        )
        # Guardar la sesión
        self._session_repository.save(session)
        return True

    def update_session_refresh_token(self, session_command: SessionCommand) -> bool:
        """Actualiza el refresh token de una sesión"""
        session = self._session_repository.get_by_client_uuid(session_command.client_uuid)
        if not session:
            raise InvalidDomainOperationException("Session", session_command.client_uuid, f"La sesión con client_uuid '{session_command.client_uuid}' no existe.")
        session.refresh_token = session_command.refresh_token
        session.token_created_at = session_command.token_created_at
        session.expires_at = session_command.expires_at
        self._session_repository.update_session_refresh_token(session)
        return True

    def get_session_by_client_uuid(self, client_uuid: str) -> Session:
        """Obtiene una sesión por client_uuid"""
        return self._session_repository.get_by_client_uuid(client_uuid)