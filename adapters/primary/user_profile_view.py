from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from infrastructure.configuration.container import Container
from domain.ports.primary.user_login_service import IUserLoginService

class UserProfileView(APIView):
    """View para obtener el perfil del usuario autenticado"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.user_login_service = Container.resolve(IUserLoginService)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                },
                'required': []
            }
        },
        responses={
            200: {
                'description': 'Datos de usuario obtenidos correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'status': {'type': 'integer'},
                    'instance': {'type': 'string'},
                    'title': {'type': 'string'},
                    'data': {'type': 'object'}
                }
            }
        }
    )
    def get(self, request):
        user_id = request.user.id
        username = request.user.username
        email = request.user.email
        role_id = request.user.role_id

        user_data = {
            'user_id': user_id,
            'username': username,
            'email': email,
            'role_id': role_id
        }

        return Response({
            'success': True,
            'status': 200,
            'instance': request.build_absolute_uri(),
            'title': 'Perfil del usuario obtenido correctamente',
            'data': user_data
        }, status=status.HTTP_200_OK)
        