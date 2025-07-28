from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from application.dto.user_registration_dto import UserRegistrationDTO
from domain.ports.primary.user_registratation_service import IUserRegistrationService
from infrastructure.configuration.container import Container
from domain.commands.user_registration_command import UserRegistrationCommand
from rest_framework.permissions import AllowAny

@extend_schema(
    tags=['users'],
    summary='Registrar nuevo usuario',
    description='Crea un nuevo usuario en el sistema con validaciones de dominio',
    examples=[
        OpenApiExample(
            'Ejemplo exitoso',
            value={
                'username': 'juan_perez',
                'password': 'password123',
                'email': 'juan@example.com',
                'role_id': 1,
                'client_uuid': '123e4567-e89b-12d3-a456-426614174000'
            },
            status_codes=['201']
        ),
        OpenApiExample(
            'Ejemplo con errores',
            value={
                'username': 'admin',  # Palabra reservada
                'password': '123',    # Muy corta
                'email': 'invalid-email',
                'role_id': 999,        # Rol inexistente
                'client_uuid': 'invalid-uuid'
            },
            status_codes=['400']
        )
    ]
)
class UserRegistrationView(APIView):
    """View para registro de usuarios (equivalente a Controller en C#)"""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._user_registration_service = None

    @property
    def user_registration_service(self):
        if self._user_registration_service is None:
            self._user_registration_service = Container.resolve(IUserRegistrationService)
        return self._user_registration_service

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'username': {'type': 'string', 'minLength': 3, 'maxLength': 50, 'pattern': '^[a-zA-Z0-9_]+$'},
                    'password': {'type': 'string', 'minLength': 6, 'maxLength': 100},
                    'email': {'type': 'string', 'format': 'email'},
                    'role_id': {'type': 'integer', 'minimum': 1},
                    'client_uuid': {'type': 'string', 'minLength': 36, 'maxLength': 36}
                },
                'required': ['username', 'password', 'email', 'role_id', 'client_uuid']
            }
        },
        responses={
            201: {
                'description': 'Usuario registrado exitosamente',
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
            },
            500: {
                'description': 'Error interno del servidor',
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
        dto = UserRegistrationDTO(**request.data)
        
        # Convertir DTO a Command

        user_command = UserRegistrationCommand(
            username=dto.username,
            password=dto.password,
            email=dto.email,
            role_id=dto.role_id,
            client_uuid=dto.client_uuid
        )
        
        # El servicio ahora maneja toda la lógica de registro y generación de tokens
        # de forma transaccional
        tokens = self.user_registration_service.register_user(user_command)
        print(tokens)
        # Devolver la respuesta con los tokens
        return Response(
            data={
                'success': True,
                'status': 201,
                'instance': 'http://localhost:8000/api/users/register',
                'title': 'Usuario registrado correctamente',
                'data': {
                    'access_token': tokens.access_token,
                    'refresh_token': tokens.refresh_token
                }
            },
            status=status.HTTP_201_CREATED
        )
        

