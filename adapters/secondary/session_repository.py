from typing import Optional, List
from domain.ports.secondary.session_repository import ISessionRepository
from domain.entities.session import Session
from infrastructure.persistence.models import Session as SessionModel
from domain.exceptions.implementations import InvalidValueException

class SessionRepository(ISessionRepository):
    """Implementación del repositorio de sesiones"""
    
    def save(self, session: Session) -> bool:
        """Guarda una nueva sesión"""
        session_model = SessionModel.from_domain_entity(session)
        session_model.save() 
        return True

    def get_by_client_uuid(self, client_uuid: str) -> Optional[Session]:
        """Obtiene una sesión por client_uuid"""
        try:
            print("Llego hasta aqui antes de obtener la sesion por client_uuid")
            print("client_uuid:", client_uuid)
            session_model = SessionModel.objects.get(client_uuid=client_uuid, is_active=True)
            print("session_model:", session_model)
            print("Llego hasta aqui despues de obtener la sesion por client_uuid")
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
            
    def update_session_refresh_token(self, session: Session) -> bool:
        """Actualiza el refresh token de una sesión"""
        session_model = SessionModel.objects.get(client_uuid=session.client_uuid)
        session_model.refresh_token = session.refresh_token
        session_model.token_created_at = session.token_created_at
        session_model.expires_at = session.expires_at
        session_model.save()
        return True

    def update_session_expiry(self, session_id: int, expires_at: int) -> bool:
        """Actualiza la fecha de expiración de una sesión"""
        try:
            session_model = SessionModel.objects.get(id=session_id)
            session_model.expires_at = expires_at
            session_model.save()
            return True
        except SessionModel.DoesNotExist:
            return False
        
    def get_session_by_uuid(self, uuid: str) -> Optional[Session]:
        """Obtiene una sesión por uuid"""
        try:
            session_model = SessionModel.objects.get(uuid=uuid)
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
    
    def get_by_id(self, session_id: int) -> Optional[Session]:
        """Obtiene una sesión por ID"""
        try:
            session_model = SessionModel.objects.get(id=session_id)
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
    
    def get_by_refresh_token(self, refresh_token: str) -> Optional[Session]:
        """Obtiene una sesión por refresh token"""
        try:
            session_model = SessionModel.objects.get(refresh_token=refresh_token, is_active=True)
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
    
    def get_by_refresh_token_and_client_uuid(self, refresh_token: str, client_uuid: str) -> Optional[Session]:
        """Obtiene una sesión por refresh token y client_uuid"""
        try:
            session_model = SessionModel.objects.get(
                refresh_token=refresh_token,
                client_uuid=client_uuid
            )
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
    
    def get_by_client_uuid_and_user(self, client_uuid: str, user_id: int) -> Optional[Session]:
        """Obtiene una sesión por client_uuid y user_id"""
        try:
            session_model = SessionModel.objects.get(
                client_uuid=client_uuid,
                user_id=user_id
            )
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            return None
    
    def update(self, session: Session) -> Session:
        """Actualiza una sesión existente"""
        try:
            session_model = SessionModel.objects.get(id=session.id)
            # Actualizar campos
            session_model.refresh_token = session.refresh_token
            session_model.client_uuid = session.client_uuid
            session_model.token_created_at = session.token_created_at
            session_model.expires_at = session.expires_at
            session_model.is_active = session.is_active
            session_model.save()
            return session_model.to_domain_entity()
        except SessionModel.DoesNotExist:
            raise InvalidValueException("sesion", session.id, "La sesión no existe")
    
    def delete(self, session_id: int) -> bool:
        """Elimina una sesión"""
        try:
            session_model = SessionModel.objects.get(id=session_id)
            session_model.delete()
            return True
        except SessionModel.DoesNotExist:
            return False
    
    def get_active_sessions_by_user(self, user_id: int) -> List[Session]:
        """Obtiene todas las sesiones activas de un usuario"""
        session_models = SessionModel.objects.filter(
            user_id=user_id, 
            is_active=True
        )
        return [session_model.to_domain_entity() for session_model in session_models] 