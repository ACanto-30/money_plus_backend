from domain.ports.primary.saving_box_box_transaction_service import ISavingBoxBoxTransactionService
from application.dto.transfer_dto import TransferDTO
from rest_framework.views import APIView
from infrastructure.configuration.container import Container
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from domain.commands.box_transfer_command import BoxTransferCommand
from django.utils import timezone
from domain.ports.primary.saving_box_service import ISavingBoxService


class SavingBoxTransactionView(APIView):
    """View para transacciones de caja"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._saving_box_box_transaction_service = None
        self._saving_box_service = None

    @property
    def saving_box_box_transaction_service(self):
        if self._saving_box_box_transaction_service is None:
            self._saving_box_box_transaction_service = Container.resolve(ISavingBoxBoxTransactionService)
        return self._saving_box_box_transaction_service

    @property
    def saving_box_service(self):
        if self._saving_box_service is None:
            self._saving_box_service = Container.resolve(ISavingBoxService)
        return self._saving_box_service

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'from_box_id': {'type': 'number'},
                    'to_box_id': {'type': 'number'},
                    'amount': {'type': 'number'},
                    'transaction_type_id': {'type': 'number'}
                },
                'required': ['from_box_id', 'to_box_id', 'amount', 'transaction_type_id']
            }
        },
        responses={
            201: {
                'description': 'Transaccion realizada correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'message': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request, saving_box_id):
        """Metodo para hacer una transaccion de una caja a la caja de ahorro"""

        # Obtener el body de la request y transformar a DTO
        dto = TransferDTO(**request.data)

        # Convertir DTO a Command
        command = BoxTransferCommand(
            user_id=request.user.id,
            from_box_id=saving_box_id,
            to_box_id=dto.to_box_id,
            amount=dto.amount,
                transaction_type_id=dto.transaction_type_id,
            created_at=timezone.now(),
            updated_at=timezone.now()
        )

        self.saving_box_box_transaction_service.make_saving_box_box_transaction(command)
        
        return Response({
            'success': True,
            'status': 201,
            'instance': 'http://localhost:8000/api/saving-box-box-transactions',
            'title': 'Transaccion realizada correctamente',
            'data': {
                'from_box_id': command.from_box_id,
                'to_box_id': command.to_box_id,
                'amount': command.amount,
            }
        })

    