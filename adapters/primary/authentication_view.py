from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from application.dto.user_login_dto import UserLoginDTO
from application.dto.authentication_dto import (
    AuthenticationResponseDTO, 
    TokenValidationDTO, 
    TokenRefreshDTO, 
    TokenRevokeDTO
)
from application.dto.refresh_acess_token_dto import RefreshAccessTokenDTO
from application.dto.refresh_refresh_token_dto import RefreshRefreshTokenDTO
from domain.ports.primary.authentication_service import IAuthenticationService
from infrastructure.configuration.container import Container
import jwt
from rest_framework.permissions import AllowAny

class RefreshRefreshToken(APIView):
    """View para autenticación de usuarios"""
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._authentication_service = None

    @property
    def authentication_service(self):
        if self._authentication_service is None:
            self._authentication_service = Container.resolve(IAuthenticationService)
        return self._authentication_service

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'client_uuid': {'type': 'string'},
                    'refresh_token': {'type': 'string'}
                },
                'required': ['client_uuid', 'refresh_token']
            }
        },
        responses={
            200: {
                'description': 'Refresh token actualizado correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def patch(self, request) -> Response:
        refresh_token_dto = RefreshRefreshTokenDTO(**request.data)

        self.authentication_service.validate_token(refresh_token_dto.refresh_token)

        # Refrescar el refresh token
        refresh_token_result = self.authentication_service.refresh_refresh_token(refresh_token_dto.client_uuid)

        return Response({
            'success': True,
            'message': 'Refresh token refrescado correctamente',
            'instance': request.build_absolute_uri(),
            'title': 'Refresh token refrescado correctamente',
            'data': {
                'refresh_token': refresh_token_result
            },
        }, status=status.HTTP_200_OK)

class RefreshAccessToken(APIView):
    """View para refrescar el access token"""
    permission_classes = [AllowAny]
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._authentication_service = None

    @property
    def authentication_service(self):
        if self._authentication_service is None:
            self._authentication_service = Container.resolve(IAuthenticationService)
        return self._authentication_service

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'refresh_token': {'type': 'string'},
                    'client_uuid': {'type': 'string'}
                },
                'required': ['refresh_token', 'client_uuid']
            }
        },
        responses={
            200: {
                'description': 'Access token actualizado correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'}
                        }
                    }  
                }
            }
        }
    )
    def patch(self, request) -> Response:
        refresh_token_dto = RefreshAccessTokenDTO(**request.data)

        # Refrescar el access token
        access_token_result = self.authentication_service.refresh_access_token(refresh_token_dto.refresh_token, refresh_token_dto.client_uuid)

        return Response({
            'success': True,
            'message': 'Access token actualizado correctamente',
            'instance': request.build_absolute_uri(),
            'title': 'Access token actualizado correctamente',
            'data': {
                'access_token': access_token_result
            },
        }, status=status.HTTP_200_OK)


    