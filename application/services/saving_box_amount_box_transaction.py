from domain.ports.primary.saving_box_amount_box_transaction_service import ISavingBoxAmountBoxTransactionService
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.commands.box_transfer_command import BoxTransferCommand
from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.ports.primary.transaction_type_service import ITransactionTypeService
from domain.ports.secondary.unit_of_work import IUnitOfWork
from infrastructure.configuration.container import Container
from domain.entities.transaction_type import TransactionTypeEnum
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from domain.ports.secondary.saving_box_amount_box_transaction_repository import ISavingBoxAmountBoxTransactionRepository
from domain.entities.saving_box_amount_box_transaction import SavingBoxAmountBoxTransaction
from django.utils import timezone

class SavingBoxAmountBoxTransactionService(ISavingBoxAmountBoxTransactionService):
    def __init__(self):
        self._saving_box_amount_box_transaction_repository = Container.resolve(ISavingBoxAmountBoxTransactionRepository)
        self._saving_box_service = Container.resolve(ISavingBoxService)
        self._amount_box_service = Container.resolve(IAmountBoxService)
        self._transaction_type_service = Container.resolve(ITransactionTypeService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._amount_box_transaction_service = Container.resolve(IAmountBoxTransactionService)
    def make_saving_box_amount_box_transaction(self, command: BoxTransferCommand) -> bool:
        """Metodo para hacer una transaccion de la caja de ahorro a otra box"""

        try:
            # EMPEZAR UNA TRANSACCION
            self._unit_of_work.begin_transaction()

            # Definir la fecha de la transaccion
            created_at = timezone.now()
            updated_at = created_at

            # Obtener la caja de ahorro origen
            saving_box = self._saving_box_service.get_saving_box_by_id(command.from_box_id)

            # Obtener la caja amount destino
            amount_box = self._amount_box_service.get_amount_box_by_id(command.to_box_id)

            # Verificar que el user_id sea el mismo para las dos cajas
            if saving_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja de ahorro", command.from_box_id, "La caja de ahorro no pertenece al usuario")
        
            if amount_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja", command.to_box_id, "La caja no pertenece al usuario")

            # Obtener el tipo de transaccion
            transaction_type = self._transaction_type_service.get_transaction_type_by_id(command.transaction_type_id)
        
            # Solamente se puede retirar de la caja de ahorro
            if transaction_type.name == TransactionTypeEnum.WITHDRAW.name:
                # Retiro
                saving_box.withdraw_amount(command.amount)
                #Cualquier otro tipo de transaccion no es valido
            else:
                raise InvalidDomainOperationException("tipo de transaccion", command.transaction_type_id, "El tipo de transaccion no es valido")

            # Suma el dinero restado a la caja de ahorro a la caja de destino
            amount_box.amount += command.amount

            # Definimos la fecha de actualizacion en updated_at
            saving_box.updated_at = updated_at

            # Actualizamos el amount de la caja de ahorro existente
            self._saving_box_service.make_saving_box_transaction(saving_box)

            # Definimos la fecha de actualizacion en updated_at
            amount_box.updated_at = updated_at

            # Creamos el command para la transaccion de la caja de destino
            amount_box_transaction_command = BoxTransactionCommand(
                box_id=command.to_box_id,
                amount=command.amount,
                transaction_type_id=TransactionTypeEnum.DEPOSIT.value,
                user_id=command.user_id,
                created_at=created_at,
                updated_at=updated_at
            )

            # Actualizamos el amount de la caja de destino existente
            self._amount_box_transaction_service.make_amount_box_transaction(amount_box_transaction_command)

            # Creamos el detalle de la transaccion
            saving_box_amount_box_transaction = SavingBoxAmountBoxTransaction(
                saving_box_id=command.from_box_id,
                amount_box_id=command.to_box_id,
                amount=command.amount,
                transaction_type_id=transaction_type.id,
                created_at=created_at,
                updated_at=updated_at
            )

            # Agregamos el detalle de la transaccion en la base de datos en la tabla saving_box_box_transaction
            self._saving_box_amount_box_transaction_repository.save(saving_box_amount_box_transaction)

            # Commit de la transaccion
            self._unit_of_work.commit()

            return True
        
        except Exception as e:
            self._unit_of_work.rollback()
            raise

    def make_amount_box_saving_box_transaction(self, saving_box_amount_box_transaction: SavingBoxAmountBoxTransaction) -> bool:
        """Metodo para hacer una transaccion de la caja amount a la caja de ahorro"""

        # Definir la fecha de la transaccion
        self._saving_box_amount_box_transaction_repository.save_transaction(saving_box_amount_box_transaction)

        return True
