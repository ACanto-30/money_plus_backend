from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from application.dto.user_registration_dto import UserRegistrationDTO
from domain.ports.primary.user_registratation_service import IUserRegistrationService
from domain.ports.primary.authentication_service import IAuthenticationService
from infrastructure.configuration.container import Container

class SessionView(APIView):
    """View para sesiones de usuarios"""
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'token': {'type': 'string'}
                },
                'required': ['token']
            }
        },
        responses={
            200: {
                'description': 'Sesión creada correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request) -> Response:
        # Aquí iría la lógica de creación de sesión

        # Si la solicitud llego aquí, significa que el token de acceso es valido
        # Porque paso por el middleware de autenticación
        # Por lo tanto, puedo obtener el user_id del request
        # 

        return Response({
            'success': True,
            'message': 'Sesión creada correctamente',
            'data': {
                'session_id': 'id_de_la_sesion'
            }
        })