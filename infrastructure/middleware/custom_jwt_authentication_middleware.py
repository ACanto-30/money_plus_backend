from rest_framework.authentication import BaseAuthentication
from rest_framework import exceptions
import jwt
from django.conf import settings
from infrastructure.exceptions.implementations.authentication_exception import AuthenticationException
from domain.ports.primary.user_service import IUserService
from infrastructure.configuration.container import Container
from infrastructure.adapters.drf_user_adapter import DRFUserAdapter

class CustomJWTAuthenticationMiddleware:
    """Middleware para autenticación JWT"""
    def authenticate(self, request):
        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        user_service = Container.resolve(IUserService)

        if not auth_header.startswith('Bearer '):
            return None

        token = auth_header.split(' ')[1]
        try:
            payload = jwt.decode(
                token,
                settings.JWT_SECRET_KEY,
                algorithms=[settings.JWT_ALGORITHM]
            )
        except jwt.ExpiredSignatureError:
            raise AuthenticationException.expired_access_token("access_token", token, "El token ha expirado")
        except jwt.InvalidTokenError:
            raise AuthenticationException.invalid_access_token("access_token", token, "El token es inválido")

        user = user_service.get_user_by_id(payload.get('user_id'))
        if not user:
            raise AuthenticationException.invalid_access_token("access_token", token, "El usuario no existe")

        return (DRFUserAdapter(user), payload)