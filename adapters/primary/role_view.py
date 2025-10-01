from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema
from application.dto.role_add_dto import RoleAddRequestDTO
from rest_framework.permissions import AllowAny
from infrastructure.configuration.container import Container
from domain.ports.primary.role_service import IRoleService
from domain.commands.role_add_command import RoleAddCommand

class RoleView(APIView):
    """View para crear un rol"""
    permission_classes = [AllowAny]

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.role_service = Container.resolve(IRoleService)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'},
                    'description': {'type': 'string'}
                },
                'required': ['name', 'description']
            }
        },
        responses={
            201: {
                'description': 'Rol creado correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'status': {'type': 'integer'},
                    'instance': {'type': 'string'},
                    'title': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'name': {'type': 'string'},
                            'description': {'type': 'string'}
                        }
                    }
                }
            }
        }
    )
    def post(self, request):
        """Crea un rol"""
        # Recibimos la data de la request en el formato de la DTO
        print("Llego hasta aqui antes de convertir el dto a command")
        role_add_request_dto = RoleAddRequestDTO(**request.data)
        print("Llego hasta aqui antes de convertir el dto a command")
        # Convertir DTO a Command
        role_add_command = RoleAddCommand(
            name=role_add_request_dto.name,
            description=role_add_request_dto.description
        )
        role = self.role_service.add_role(role_add_command)
        return Response({
            'success': True,
            'status': 201,
            'instance': 'http://localhost:8000/api/roles',
            'title': 'Rol creado correctamente',
            'data': {
                'name': role.name,
                'description': role.description,
            }
        })

