from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from infrastructure.configuration.container import Container
from domain.ports.primary.clean_box_service import ICleanBoxService
from rest_framework import status
from application.dto.clean_up_event_dto import BoxCleanUpEventResponseDTO

class CleanUpView(APIView):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.clean_box_service = Container.resolve(ICleanBoxService)
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
    def post(self, request):

        print("En la view:", request.user.id)
        user_id = request.user.id

        print(user_id)

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/clean-up',
                'title': 'User ID is required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        self.clean_box_service.clean_all_boxes_by_user_id(user_id)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/clean-up',
            'title': 'Cajas limpiadas correctamente',
            'data': {}
        }, status=status.HTTP_200_OK)
    
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
    # Metodo para obtener todas las limpiezas de cajas por usuario, con su fecha y monto total
    def get(self, request):
        print("En la view:", request.user.id)
        user_id = request.user.id

        print(user_id)

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/clean-up/boxes',
                'title': 'User ID is required',
                'data': {}
            }, status=status.HTTP_400_BAD_REQUEST)

        print("Llego hasta aqui antes de obtener las limpiezas de cajas")
        box_clean_up_events = self.clean_box_service.get_all_box_clean_up_events_by_user_id(user_id)
        print("Llego hasta aqui despues de obtener las limpiezas de cajas")
        print("box_clean_up_events:", box_clean_up_events)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/clean-up/boxes',
            'title': 'Limpiezas de cajas obtenidas correctamente',
            'data': {
                'box_clean_up_events': [BoxCleanUpEventResponseDTO.from_entity(box_clean_up_event).model_dump() for box_clean_up_event in box_clean_up_events]
            }
        }, status=status.HTTP_200_OK)