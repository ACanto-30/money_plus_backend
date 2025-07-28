from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from application.dto.user_login_dto import UserLoginDTO
from domain.ports.primary.user_login_service import IUserLoginService
from infrastructure.configuration.container import Container
from domain.commands.user_login_command import UserLoginCommand
from rest_framework.permissions import AllowAny

class UserLoginView(APIView):
    """View para login de usuarios"""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user_login_service = None
    
    @property
    def user_login_service(self):
        if self._user_login_service is None:
            self._user_login_service = Container.resolve(IUserLoginService)
        return self._user_login_service

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'email': {'type': 'string', 'format': 'email'},
                    'password': {'type': 'string', 'minLength': 6, 'maxLength': 100},
                    'client_uuid': {'type': 'string', 'minLength': 36, 'maxLength': 36}
                },
                'required': ['email', 'password', 'client_uuid']
            }
        },
        responses={
            200: {
                'description': 'Login exitoso',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'access_token': {'type': 'string'},
                            'refresh_token': {'type': 'string'}
                        }
                    }
                }
            },
            400: {
                'description': 'Error de validación',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'},
                    'errors': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'field': {'type': 'string'},
                                'message': {'type': 'string'},
                                'type': {'type': 'string'}
                            }
                        }
                    }
                }
            }
        }
    )
    def post(self, request):
        # Dejamos que las excepciones de Pydantic se propaguen al DRF exception handler
        dto = UserLoginDTO(**request.data)

        print("dto:", dto)

        print("Llego hasta aqui antes de convertir el dto a command")
        
        # Convertir DTO a Command
        from domain.commands.user_login_command import UserLoginCommand
        user_command = UserLoginCommand(
            email=dto.email,
            password=dto.password,
            client_uuid=dto.client_uuid
        )
        
        tokens = self.user_login_service.login(user_command)
        
        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/users/login',
            'title': 'Login exitoso',
            'data': {
                'access_token': tokens.access_token,
                'refresh_token': tokens.refresh_token
            }
        }, status=status.HTTP_200_OK)

    