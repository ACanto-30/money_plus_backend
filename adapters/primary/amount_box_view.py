from rest_framework.views import APIView

from domain.ports.primary.amount_box_service import IAmountBoxService
from infrastructure.configuration.container import Container
from rest_framework.response import Response
from application.dto.amount_box_response_dto import AmountBoxResponseDTO
from drf_spectacular.utils import extend_schema

class AmountBoxView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._amount_box_service = None

    @property
    def amount_box_service(self):
        return Container.resolve(IAmountBoxService)

    @extend_schema(
        responses={
            200: {
                'description': 'Caja de ahorro obtenida correctamente',
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
        amount_box = self.amount_box_service.get_amount_box_by_user_id(user_id)
        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/amount-box',
            'title': 'Caja de ahorro obtenida correctamente',
            'data': {
                'amount_box': AmountBoxResponseDTO.from_entity(amount_box).model_dump()
            }
        })