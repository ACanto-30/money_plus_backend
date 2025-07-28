from domain.ports.primary.saving_box_box_transaction_service import ISavingBoxBoxTransactionService
from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from application.dto.amount_box_transaction_dto import AmountBoxTransactionDTO
from rest_framework.views import APIView
from infrastructure.configuration.container import Container
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema, OpenApiParameter
from domain.commands.box_transaction_command import BoxTransactionCommand
from django.utils import timezone
from application.dto.transfer_dto import TransferDTO

class AmountBoxTransactionView(APIView):
    """View para transacciones de caja"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._amount_box_transaction_service = None

    @property
    def amount_box_transaction_service(self):
        if self._amount_box_transaction_service is None:
            self._amount_box_transaction_service = Container.resolve(IAmountBoxTransactionService)
        return self._amount_box_transaction_service


    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'amount': {'type': 'number'},
                    'transaction_type_id': {'type': 'number'}
                },
                'required': ['amount', 'transaction_type_id']
            }
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description='Bearer token JWT',
                required=True,
                type=str
            )
        ],
        responses={
            200: {
                'description': 'Transaccion obtenida correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request, amount_box_id):
        """Metodo para hacer una transaccion en la caja"""

        # Obtener el body de la request y transformar a DTO
        dto = AmountBoxTransactionDTO(**request.data)

        print(dto)

        print("En la view:", request.user.id)
        user_id = request.user.id

        if user_id is None:
            return Response({
                'success': False,
                'status': 400,
                'instance': 'http://localhost:8000/api/amount-boxes-transactions',
                'title': 'User ID es requerido',
            }, status=status.HTTP_400_BAD_REQUEST)

        print("amount_box_id antes de hacer el command:", amount_box_id)

        # Convertir DTO a Command
        command = BoxTransactionCommand(
            box_id=amount_box_id,
            amount=dto.amount,
            transaction_type_id=dto.transaction_type_id,
            user_id=user_id if user_id is not None else 0,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        self.amount_box_transaction_service.make_amount_box_transaction(command)
        
        return Response({
            'success': True,
            'status': 201,
            'instance': 'http://localhost:8000/api/amount-boxes-transactions',
            'title': 'Transaccion realizada correctamente',
            'data': {
                'amount_box_id': command.box_id,
                'amount': command.amount,
            }
        })

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'amount_box_id': {'type': 'number'},
                    'amount': {'type': 'number'},
                    'transaction_type_id': {'type': 'number'}
                },
                'required': ['amount_box_id', 'amount', 'transaction_type_id']
            }
        },
        parameters=[
            OpenApiParameter(
                name='Authorization',
                location=OpenApiParameter.HEADER,
                description='Bearer token JWT',
                required=True,
                type=str
            )
        ],
        responses={
            200: {
                'description': 'Transaccion obtenida correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def get(self, request):
        """Metodo para obtener el monto de la caja"""
        print("En la view:", request.user.id)
        print("En la view:", request.user.username)
        print("En la view:", request.user.email)
        print("En la view:", request.user.role_id)

        amount_box_transaction = self.amount_box_transaction_service.get_total_amount_box_by_user_id(request.user.id)

        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/amount-boxes-transactions',
            'title': 'Monto de la caja obtenida correctamente',
            'data': {
                'amount': amount_box_transaction,
            }
        })