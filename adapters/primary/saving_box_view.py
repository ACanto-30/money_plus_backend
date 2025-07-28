from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from infrastructure.configuration.container import Container
from domain.ports.primary.saving_box_service import ISavingBoxService
from application.dto.saving_box_response_dto import SavingBoxResponseDTO

class SavingBoxView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    @property
    def saving_box_service(self):
        return Container.resolve(ISavingBoxService)

    @extend_schema(
        responses={
            200: {
                'description': 'Transaccion obtenida correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'status': {'type': 'number'},
                    'instance': {'type': 'string'},
                    'title': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'amount': {'type': 'number'}
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        """Metodo para obtener el monto de la caja de ahorro"""
        user_id = request.user.id

        saving_box = self.saving_box_service.get_saving_box_by_user_id(user_id)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/saving-box',
            'title': 'Caja de ahorro obtenida correctamente',
            'data': {
                'saving_box': SavingBoxResponseDTO.from_entity(saving_box).model_dump()
            }
        })


