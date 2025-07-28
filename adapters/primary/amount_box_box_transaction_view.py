from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema
from rest_framework.response import Response
from domain.commands.box_transfer_command import BoxTransferCommand
from django.utils import timezone
from infrastructure.configuration import Container
from domain.ports.primary.amount_box_box_transaction_service import IAmountBoxBoxTransactionService
from application.dto.amount_box_box_transaction_dto import AmountBoxBoxTransactionDTO

class AmountBoxBoxTransactionView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)  

    @property
    def amount_box_box_transaction_service(self):
        return Container.resolve(IAmountBoxBoxTransactionService)

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'from_box_id': {'type': 'number'},
                    'amount': {'type': 'number'},
                    'transaction_type_id': {'type': 'number'}
                },
                'required': ['from_box_id', 'amount', 'transaction_type_id']
            }
        },
        responses={
            200: {
                'description': 'Transacciones obtenidas correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'status': {'type': 'integer'},
                    'instance': {'type': 'string'},
                    'title': {'type': 'string'},
                    'data': {'type': 'object'}
                }
            },
            400: {
                'description': 'Error al obtener las transacciones',
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
    def post(self, request, box_id):

        # Obtener el body de la request y transformar a DTO
        dto = AmountBoxBoxTransactionDTO(**request.data)

        print(dto)
        print(box_id)
        print("Llego hasta aqui")

        # Convertir DTO a Command
        command = BoxTransferCommand(
            from_box_id=dto.from_box_id,
            to_box_id=box_id,
            amount=dto.amount,
            transaction_type_id=dto.transaction_type_id,
            user_id=request.user.id,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        self.amount_box_box_transaction_service.make_amount_box_box_transaction(command)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/amount-box-box-transactions',
            'title': 'Transacciones obtenidas correctamente',
        })