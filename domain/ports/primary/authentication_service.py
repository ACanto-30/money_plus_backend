from abc import ABC, abstractmethod
from domain.commands.access_token_payload_command import AccessTokenPayloadCommand
from domain.commands.decoded_token_command import DecodedTokenCommand

class IAuthenticationService(ABC):
    """Puerto primario para el servicio de autenticación"""
    
    @abstractmethod
    def hash_password(self, password: str) -> str:
        """Hashea una contraseña usando SHA-256"""
        pass

    @abstractmethod
    def verify_password(self, password: str, hashed_password: str) -> bool:
        """Verifica una contraseña contra su hash"""
        pass

    @abstractmethod
    def generate_refresh_token(self, user_id: int) -> str:
        """Genera un token de refresco"""
        pass

    @abstractmethod
    def generate_access_token(self, access_token_payload: AccessTokenPayloadCommand, expires_in: int) -> str:
        """Genera un token de acceso"""
        pass

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        """Valida un token JWT"""
        pass

    @abstractmethod
    def refresh_refresh_token(self, refresh_token: str, client_uuid: str) -> str:
        """Refresca un token JWT"""
        pass

    @abstractmethod
    def refresh_access_token(self, refresh_token: str, client_uuid: str) -> str:
        """Refresca un token de acceso"""
        pass
    
    @abstractmethod
    def revoke_access_token(self, token: str) -> bool:
        """Revoca un token de acceso"""
        pass
    
    @abstractmethod
    def revoke_refresh_token(self, token: str) -> bool:
        """Revoca un token de refresco"""
        pass
    
    @abstractmethod
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
        pass