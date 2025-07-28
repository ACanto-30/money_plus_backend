from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

from infrastructure.configuration.container import Container
from domain.ports.primary.box_service import IBoxService
from application.dto.box_creation_dto import BoxCreationResponseDTO
from application.dto.box_creation_dto import BoxCreationRequestDTO
from application.dto.box_creation_dto import BoxRenameRequestDTO


class BoxView(APIView):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.box_service = Container.resolve(IBoxService)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                },
                'required': []
            }
        }
    )
    def get(self, request, id):
        user_id = request.user.id
        print(user_id)

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': request.build_absolute_uri(),
                'title': 'User ID es requerido',
                'errors': ['User ID es requerido']
            }, status=status.HTTP_400_BAD_REQUEST)

        self.box_service.is_owner_box(id, user_id)

        box = self.box_service.get_box_by_id(id)

        return Response({
            'success': True,
            'status': 200,
            'instance': request.build_absolute_uri(),
            'title': 'Datos de usuario obtenidos correctamente',
            'data': BoxCreationResponseDTO.from_entity(box).model_dump(),
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'box_id': {'type': 'integer'}
                },
                'required': ['box_id']
            }
        },
        responses={
            200: {
                'description': 'Caja desactivada correctamente',
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
    def delete(self, request, id):
        print("En la view:", request.user.id)
        user_id = request.user.id

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/boxes',
                'title': 'User ID is required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        self.box_service.deactive_box(id, user_id)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/boxes',
            'title': 'Caja desactivada correctamente',
            'data': {
                'box': {
                    'id': id
                }
            }
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}  
                },
                'required': ['name']
            }
        },
        responses={
            200: {  
                'description': 'Caja actualizada correctamente',
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
    def patch(self, request, id):
        """Metodo para actualizar el nombre de la caja"""
        user_id = request.user.id

        box_rename_dto = BoxRenameRequestDTO(**request.data)

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/boxes',
                'title': 'User ID is required',
                'errors': ['User ID is required']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        box = self.box_service.update_box_name(id, box_rename_dto.name)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/boxes',
            'title': 'Caja actualizada correctamente',
            'data': {
                'box': BoxCreationResponseDTO.from_entity(box).model_dump()
            }
        }, status=status.HTTP_200_OK)

class BoxCreateView(APIView):

    def __init__(self, **kwargs):

        super().__init__(**kwargs)
        self.box_service = Container.resolve(IBoxService)

    @extend_schema(

        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'name': {'type': 'string'}
                },
                'required': ['name']
            }
        },
        responses={
            200: {
                'description': 'Caja creada correctamente',
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
    def post(self, request):

        box_dto = BoxCreationRequestDTO(**request.data)
        user_id = request.user.id

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/boxes',
                'title': 'User ID is required',
                'errors': ['User ID is required']
            }, status=status.HTTP_400_BAD_REQUEST)

        box = self.box_service.save_box(user_id, box_dto.name)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/boxes',
            'title': 'Caja creada correctamente',
            'data': {
                'box': BoxCreationResponseDTO.from_entity(box).model_dump()
            }
        }, status=status.HTTP_200_OK)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {},
                'required': []
            }
        },
        responses={
            200: {
                'description': 'Cajas obtenidas correctamente',
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

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': request.build_absolute_uri(),
                'title': 'User ID es requerido',
                'errors': ['User ID es requerido']
            }, status=status.HTTP_400_BAD_REQUEST)

        boxes = self.box_service.get_all_boxes_active_by_user_id(user_id)
        # Serializa cada box usando tu DTO
        boxes_data = [BoxCreationResponseDTO.from_entity(box).model_dump() for box in boxes]

        return Response({
            'success': True,
            'status': 200,
            'instance': request.build_absolute_uri(),
            'title': 'Cajas obtenidas correctamente',
            'data': {
                'boxes': boxes_data
            }
        }, status=status.HTTP_200_OK)

