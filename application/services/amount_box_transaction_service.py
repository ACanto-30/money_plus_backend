from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.secondary.amount_box_transaction_repository import IAmountBoxTransactionRepository
from domain.ports.secondary.unit_of_work import IUnitOfWork
from infrastructure.configuration.container import Container
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from domain.entities.amount_box_transaction import AmountBoxTransaction
from domain.ports.secondary.transaction_type_repository import TransactionTypeEnum
from domain.ports.primary.transaction_type_service import ITransactionTypeService
from django.utils import timezone

class AmountBoxTransactionService(IAmountBoxTransactionService):
    def __init__(self):
        self._amount_box_transaction_repository = Container.resolve(IAmountBoxTransactionRepository)
        self._amount_box_service = Container.resolve(IAmountBoxService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._transaction_type_service = Container.resolve(ITransactionTypeService)

    def make_amount_box_transaction(self, command: BoxTransactionCommand) -> bool:
        """Metodo para hacer una transaccion en la caja"""

        try:

            # Definir la fecha de la transaccion
            created_at = command.created_at
            updated_at = command.updated_at

            # EMPEZAR UNA TRANSACCION con begin_transaction
            self._unit_of_work.begin_transaction()

            # Obtener la caja
            print(f"command.box_id: {command.box_id}")
            amount_box = self._amount_box_service.get_amount_box_by_id(command.box_id)
            print("amount_box:", amount_box, type(amount_box))

            # Verificar si la caja existe
            if not amount_box:
                raise InvalidDomainOperationException("caja", command.box_id, "La caja no existe")

            # Verificar si el usuario tiene permisos para hacer la transaccion
            if amount_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("usuario", command.user_id, "El usuario no tiene permisos para hacer la transaccion")

            # Verificar si el tipo de transaccion es valido contra la base de datos
            transaction_type = self._transaction_type_service.get_transaction_type_by_id(command.transaction_type_id)
            if not transaction_type:
                raise InvalidDomainOperationException("tipo de transaccion", command.transaction_type_id, "El tipo de transaccion no existe")
            print("transaction_type:", transaction_type, type(transaction_type))
            print("created_at:", created_at, type(created_at))
            print("updated_at:", updated_at, type(updated_at))
            # Hacer la transaccion, crear el nuevo amount_box_transaction
            
            # Evaluar el tipo de transacción, si es de retiro o deposito
            if transaction_type.name == TransactionTypeEnum.DEPOSIT.name:
                # Deposito
                amount_box.amount += command.amount # Aumentar el saldo de la caja
            elif transaction_type.name == TransactionTypeEnum.WITHDRAW.name:
                # Retiro
                amount_box.withdraw_amount(command.amount) # Disminuir el saldo de la caja
            elif transaction_type.name == TransactionTypeEnum.CLEAN_BOX.name:
                # Limpiar caja
                amount_box.clean() # Limpiar la caja
            else:
                raise InvalidDomainOperationException("transaccion", command.transaction_type_id, "No se permiten retiros de la caja")

            # Crear la transaccion
            print("amount_box:", amount_box, type(amount_box))
            print("transaction_type:", transaction_type, type(transaction_type))
            print("transaction_type.id en el service amount_box_transaction_service:", transaction_type.id, type(transaction_type.id))
            amount_box_transaction = AmountBoxTransaction(
                amount_box_id=amount_box.id,
                amount=command.amount,
                transaction_type_id=transaction_type.id,
                created_at=created_at,
                updated_at=updated_at
            )

            # Guardar la transaccion en la base de datos
            print("amount_box_transaction:", amount_box_transaction, type(amount_box_transaction))
            self._amount_box_transaction_repository.make_amount_box_transaction(amount_box_transaction)

            # Actualizar el saldo de la caja
            self._amount_box_service.make_amount_box_transaction(amount_box)

            # Commit de la transaccion
            self._unit_of_work.commit()

            return True

        except Exception as e:
            # Rollback de la transaccion
            self._unit_of_work.rollback()
            raise

    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        """Metodo para obtener el monto de la caja de ahorro"""
        amount_box = self._amount_box_service.get_amount_box_by_user_id(user_id)
        if not amount_box:
            raise InvalidDomainOperationException("caja", user_id, "La caja no existe")
        return amount_box.amount