from decouple import config
from typing import Optional, Dict, Any
from domain.ports.primary.authentication_service import IAuthenticationService
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.ports.primary.user_service import IUserService
from domain.ports.primary.session_service import ISessionService
from domain.entities.session import Session
from domain.commands.access_token_payload_command import AccessTokenPayloadCommand
from domain.commands.decoded_token_command import DecodedTokenCommand
from domain.commands.session_command import SessionCommand
from infrastructure.configuration.container import Container
from domain.exceptions.implementations import InvalidDomainOperationException
import hashlib
import hmac
import secrets
from datetime import datetime, timedelta, timezone
import jwt
from django.conf import settings
from infrastructure.exceptions.implementations.authentication_exception import AuthenticationException

class AuthenticationService(IAuthenticationService):
    """Servicio de aplicación para autenticación JWT"""
    
    def __init__(self):
        self._user_service = Container.resolve(IUserService)
        self._session_service = Container.resolve(ISessionService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        # En producción, esto debería venir de configuración
        self._jwt_secret = str(settings.JWT_SECRET_KEY)
        self._jwt_algorithm = str(settings.JWT_ALGORITHM)
        self._access_token_expiry = int(config('JWT_EXPIRATION_TIME_ACCESS_TOKEN', 3600))
        self._refresh_token_expiry = int(config('JWT_EXPIRATION_TIME_REFRESH_TOKEN', 604800))

    def hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        return hmac.compare_digest(self.hash_password(password), hashed_password)
    
    def generate_refresh_token(self, user_id: int) -> str:
        """Genera un token de refresco"""
        return jwt.encode(
            {
                'exp': datetime.now(timezone.utc) + timedelta(seconds=self._refresh_token_expiry),
                'iat': datetime.now(timezone.utc),
                'user_id': user_id,
            },
            self._jwt_secret,
            algorithm=self._jwt_algorithm
        )

    def generate_access_token(self, access_token_payload: AccessTokenPayloadCommand, expires_in: int) -> str:
        """Genera un token de acceso"""
        payload = access_token_payload.__dict__
        payload['exp'] = datetime.now(timezone.utc) + timedelta(seconds=expires_in)
        payload['iat'] = datetime.now(timezone.utc)
        return jwt.encode(payload, self._jwt_secret, algorithm=self._jwt_algorithm)

    def validate_token(self, token: str) -> bool:
        """Valida un token JWT"""
        try:
            payload = jwt.decode(token, self._jwt_secret, algorithms=[self._jwt_algorithm])
            return True
        except jwt.ExpiredSignatureError:
            raise AuthenticationException.expired_access_token("access_token", token, "El token ha expirado")
        except jwt.InvalidTokenError:
            raise AuthenticationException.invalid_access_token("access_token", token, "El token es inválido")
    
    def refresh_refresh_token(self, uuid: str) -> str:
        """Refresca un token de refresco"""

        try:
            # EMPEZAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()

            # Obtener el session_id de la base de datos (session_id)
            session = self._session_service.get_session_by_client_uuid(uuid)
            if not session:
                raise InvalidDomainOperationException.session_not_found(session.uuid)
            
            # Decodificar el refresh token
            refresh_token = jwt.decode(session.refresh_token, self._jwt_secret, algorithms=[self._jwt_algorithm])

            # Generar nuevo refresh token reutilizando la función de generación
            new_refresh_token = self.generate_refresh_token(refresh_token['user_id'])
            
            # Obtener la fecha de expiración del nuevo refresh token
            refresh_token_expiry = jwt.decode(new_refresh_token, self._jwt_secret, algorithms=[self._jwt_algorithm])['exp']

            expires_at = datetime.fromtimestamp(refresh_token_expiry, tz=timezone.utc)

            # Crear el payload para la sesión
            session_command = SessionCommand(
                user_id=refresh_token['user_id'],
                refresh_token=new_refresh_token,
                client_uuid=uuid,
                token_created_at=datetime.now(timezone.utc),
                expires_at=expires_at
            )

            # Actualizar la sesión en la base de datos
            self._session_service.update_session_refresh_token(session_command)

            # Hacer commit de la transacción
            self._unit_of_work.commit()

            return new_refresh_token
        except jwt.ExpiredSignatureError:
            self._unit_of_work.rollback_transaction()
            raise InvalidDomainOperationException("RefreshToken", uuid, "Refresh token expirado")
        except jwt.InvalidTokenError:
            self._unit_of_work.rollback_transaction()
            raise InvalidDomainOperationException("RefreshToken", uuid, "Refresh token inválido")
    
    def refresh_access_token(self, refresh_token: str, client_uuid: str) -> str:
        """Refresca un token de acceso"""
        try:
            # EMPEZAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()

            # Decodificar el refresh token
            payload_refresh_token = jwt.decode(refresh_token, self._jwt_secret, algorithms=[self._jwt_algorithm])
            
            # Como el payload trae el user_id, se puede obtener los datos del usuario en la base de datos
            user = self._user_service.get_user_by_id(payload_refresh_token.get('user_id'))
            if not user:
                self._unit_of_work.rollback_transaction()
                raise InvalidDomainOperationException("User", payload_refresh_token.get('user_id'), "Usuario no encontrado")

            # Crear el payload para el access token
            payload = AccessTokenPayloadCommand(
                user_id=user.id,
                username=user.username,
                email=user.email.value,
                role_id=user.role_id,
                client_uuid=client_uuid
            )
            # Generar nuevo access token
            new_access_token = self.generate_access_token(payload, self._access_token_expiry)

            # FINALIZAR TRANSACCIÓN
            self._unit_of_work.commit()

            return new_access_token

        except jwt.ExpiredSignatureError:
            self._unit_of_work.rollback_transaction()
            raise InvalidDomainOperationException("RefreshToken", refresh_token, "Refresh token expirado")
        except jwt.InvalidTokenError:
            self._unit_of_work.rollback_transaction()
            raise InvalidDomainOperationException("RefreshToken", refresh_token, "Refresh token inválido")
    
    def revoke_access_token(self, token: str) -> bool:
        """Revoca un token de acceso"""
        # En una implementación real, agregarías el token a una lista negra
        # o lo invalidarías en la base de datos
        return True
    
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoca un token de refresco"""
        # En una implementación real, agregarías el token a una lista negra
        # o lo invalidarías en la base de datos
        return True
    
    def decode_refresh_token(self, refresh_token: str) -> DecodedTokenCommand:
        """
        Decodifica un refresh token y retorna sus datos
        
        Args:
            refresh_token: Token JWT de refresco
            
        Returns:
            DecodedTokenCommand con user_id, iat y exp
            
        Raises:
            InvalidDomainOperationException: Si el token es inválido o expirado
        """
        try:
            payload = jwt.decode(refresh_token, self._jwt_secret, algorithms=[self._jwt_algorithm])
            
            return DecodedTokenCommand(
                user_id=payload.get('user_id'),
                iat=payload.get('iat'),
                exp=payload.get('exp')
            )
            
        except jwt.ExpiredSignatureError:
            raise InvalidDomainOperationException("RefreshToken", refresh_token, "Refresh token expirado")
        except jwt.InvalidTokenError:
            raise InvalidDomainOperationException("RefreshToken", refresh_token, "Refresh token inválido")
