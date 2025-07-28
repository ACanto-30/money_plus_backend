from domain.ports.secondary.amount_box_box_transaction_repository import IAmountBoxBoxTransactionRepository
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.ports.primary.box_transaction_service import IBoxTransactionService
from domain.ports.primary.box_service import IBoxService
from domain.ports.primary.transaction_type_service import ITransactionTypeService
from domain.ports.primary.user_service import IUserService
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.commands.box_transfer_command import BoxTransferCommand
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from domain.ports.secondary.transaction_type_repository import TransactionTypeEnum
from domain.entities.amount_box_box_transaction import AmountBoxBoxTransaction
from datetime import datetime, timezone
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from domain.ports.primary.amount_box_box_transaction_service import IAmountBoxBoxTransactionService
from infrastructure.configuration.container import Container

class AmountBoxBoxTransactionService(IAmountBoxBoxTransactionService):
    def __init__(self):
        self._amount_box_box_transaction_repository = Container.resolve(IAmountBoxBoxTransactionRepository)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._box_service = Container.resolve(IBoxService)
        self._transaction_type_service = Container.resolve(ITransactionTypeService)
        self._user_service = Container.resolve(IUserService)
        self._amount_box_service = Container.resolve(IAmountBoxService)
        self._amount_box_transaction_service = Container.resolve(IAmountBoxTransactionService)

    def make_amount_box_box_transaction(self, command: BoxTransferCommand) -> bool:
        """Metodo para hacer una transaccion en la caja"""

        try:
            print("Llego hasta aqui antes de definir la fecha de actualizacion en updated_at")
            self._unit_of_work.begin_transaction()
            # Definir la fecha de actualizacion en updated_at
            updated_at = datetime.now(timezone.utc)
            created_at = datetime.now(timezone.utc)

            # Obtener la caja de origen que es un amount_box
            from_box = self._amount_box_service.get_amount_box_by_id(command.from_box_id)

            # Obtener la caja de destino que es un box normal
            to_box = self._box_service.get_box_by_id(command.to_box_id)

            # Verificar si el usuario tiene permisos para hacer la transaccion
            print("Llego hasta aqui")
            print("command.user_id:", command.user_id)
            print("from_box.user_id:", from_box.user_id)
            print("from_box.amount:", from_box.amount)
            print("to_box.amount:", to_box.amount)
            print("to_box.user_id:", to_box.user_id)

            if from_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja", command.from_box_id, "La caja no pertenece al usuario")
            
            if to_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja", command.to_box_id, "La caja no pertenece al usuario")

            # Verificar si el tipo de transaccion es valido
            transaction_type = self._transaction_type_service.get_transaction_type_by_id(command.transaction_type_id)
            if transaction_type is None:
                raise InvalidDomainOperationException("transaccion", command.transaction_type_id, "El tipo de transaccion no es valido")

            print("Llego hasta aqui antes de hacer la transaccion")

            # Hacer la transaccion, solo se permite depositos en la caja, de no ser asi se lanza directamente una excepcion
            if transaction_type.name == TransactionTypeEnum.DEPOSIT.name:
                # Deposito
                to_box.amount += command.amount
            else:
                raise InvalidDomainOperationException("transaccion", command.transaction_type_id, "No se permiten retiros de la caja")

            print("Llego hasta aqui antes de guardar la transaccion")

            print("from_box.amount:", from_box.amount)
            print("to_box.amount:", to_box.amount)

            # Guardar la transaccion
            amount_box_box_transaction = AmountBoxBoxTransaction(
                amount_box_id=from_box.id,
                box_id=command.to_box_id,
                amount=command.amount,
                transaction_type_id=transaction_type.id,
                created_at=created_at,
                updated_at=updated_at
            )


            # Guardar la transaccion
            self._amount_box_box_transaction_repository.save(amount_box_box_transaction)

            # Creamos el command para la transaccion de la caja de destino
            amount_box_transaction_command = BoxTransactionCommand(
                box_id=command.from_box_id,
                amount=command.amount,
                transaction_type_id=TransactionTypeEnum.WITHDRAW.value,
                user_id=command.user_id,
                created_at=created_at,
                updated_at=updated_at
            )

            print("Llego hasta aqui antes de hacer la transaccion de la caja")
            # Guardar la caja
            self._amount_box_transaction_service.make_amount_box_transaction(amount_box_transaction_command)

            print("Llego hasta aqui despues de hacer la transaccion de la caja")
            # Guardar la box normal
            self._box_service.make_box_transaction(to_box)
            print("Llego hasta aqui despues de guardar la box normal")

            self._unit_of_work.commit()
            return True

        except Exception as e:
            self._unit_of_work.rollback()
            raise