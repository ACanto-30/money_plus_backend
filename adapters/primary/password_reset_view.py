from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from application.dto.password_reset_dto import PasswordResetRequestDTO, PasswordResetDTO
from domain.ports.primary.password_reset_service import IPasswordResetService
from infrastructure.configuration.container import Container
from django.utils import timezone
from datetime import timedelta
from rest_framework.permissions import AllowAny

class PasswordResetView(APIView):
    """View para reseteo de contraseña"""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._password_reset_service = Container.resolve(IPasswordResetService)


    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'}
                },
                'required': ['email']
            }
        },
        responses={
            200: {
                'description': 'Reseteo de contraseña exitoso',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }   
        }
    )
    def post(self, request):
        dto = PasswordResetRequestDTO(**request.data)
        
        self._password_reset_service.password_reset_request(dto.email)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/users/password-reset',
            'title': 'Solicitud de reseteo de contraseña exitosa',
        })

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer'},
                    'new_password': {'type': 'string'},
                    'email': {'type': 'string', 'format': 'email'}
                },
                'required': ['code', 'new_password', 'email']
            }
        },
        responses={
            200: {
                'description': 'Reseteo de contraseña exitoso',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def patch(self, request):
        dto = PasswordResetDTO(**request.data)
        self._password_reset_service.password_reset(dto.code, dto.new_password, dto.email)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/users/password-reset',
            'title': 'Reseteo de contraseña exitoso, por favor inicie sesión con su nueva contraseña',
        })

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'code': {'type': 'integer'}
                },
                'required': ['code']
            }
        },
        responses={
            200: {
                'description': 'Verificación de código de reseteo exitosa',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def get(self, request):

        # Obtener el código enviando para verificar si el código es valido
        code = request.query_params.get('code')

        # Verificar si el código es valido
        is_valid_code = self._password_reset_service.verify_code(code)

        if not is_valid_code:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/users/password-reset',
                'title': 'El código de reseteo no es valido',
            })
        # Si el código es valido, se debe retornar un mensaje de éxito

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/users/password-reset',
            'title': 'El código de reseteo es valido',
        })
