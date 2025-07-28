from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from application.dto.transaction_dto import TransactionDTO
from domain.ports.primary.box_transaction_service import IBoxTransactionService
from domain.commands.box_transaction_command import BoxTransactionCommand
from infrastructure.configuration.container import Container
from domain.ports.secondary.transaction_type_repository import TransactionTypeEnum
from django.utils import timezone
from drf_spectacular.utils import extend_schema

class BoxTransactionView(APIView):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.box_transaction_service = Container.resolve(IBoxTransactionService)

    @extend_schema(
        summary="Hacer una transaccion en la caja",
        description="Hace una transaccion en la caja",
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'amount': {'type': 'integer'},
                    'transaction_type_id': {'type': 'integer'}
                },
                'required': ['amount', 'transaction_type_id']
            }
        },
        responses={
            200: {
                'description': 'Transaccion realizada correctamente',
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
        user_id = request.user.id
        box_transaction_dto = TransactionDTO(**request.data)

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/box-transactions',
                'title': 'User ID is required',
                'errors': ['User ID is required']
            }, status=status.HTTP_400_BAD_REQUEST)

        box_transaction = BoxTransactionCommand(
            user_id=user_id,
            box_id=box_id,
            amount=box_transaction_dto.amount,
            transaction_type_id=TransactionTypeEnum.WITHDRAW.value,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        box_transaction = self.box_transaction_service.make_box_transaction(box_transaction)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/box-transactions',
            'title': 'Transaccion realizada correctamente',
            'data': {
                'box': {
                    'id': box_transaction.box_id,
                    'amount': box_transaction.amount,
                }
            }
        })
