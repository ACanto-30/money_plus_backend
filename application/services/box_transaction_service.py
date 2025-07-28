from domain.ports.primary.box_transaction_service import IBoxTransactionService
from domain.ports.secondary.box_transaction_repository import IBoxTransactionRepository

from domain.entities.box_transaction import BoxTransaction
from domain.ports.primary.box_service import IBoxService
from infrastructure.configuration.container import Container
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.ports.secondary.transaction_type_repository import TransactionTypeEnum
from domain.ports.primary.transaction_type_service import ITransactionTypeService

class BoxTransactionService(IBoxTransactionService):
    def __init__(self):
        self.box_transaction_repository = Container.resolve(IBoxTransactionRepository)
        self.box_service = Container.resolve(IBoxService)
        self.unit_of_work = Container.resolve(IUnitOfWork)
        self.transaction_type_service = Container.resolve(ITransactionTypeService)

    def make_box_transaction(self, box_transaction: BoxTransaction) -> BoxTransaction:

        try:
            self.unit_of_work.begin_transaction()
            # Verificar si la caja existe
            box = self.box_service.get_box_by_id(box_transaction.box_id)

            if not box:
                raise InvalidDomainOperationException("caja", box_transaction.box_id, "La caja no existe")
            
            # Verificar tipo de transaccion
            transaction_type = self.transaction_type_service.get_transaction_type_by_id(box_transaction.transaction_type_id)
            if transaction_type.id == TransactionTypeEnum.WITHDRAW.value:
                box.withdraw_amount(box_transaction.amount)
            else:
                raise InvalidDomainOperationException("transaccion", box_transaction.transaction_type_id, "El tipo de transaccion no es valido")

            # Actualiza saldo de la caja
            self.box_service.make_box_transaction(box)

            # Hacer la transaccion
            self.box_transaction_repository.make_box_transaction(box_transaction)

            self.unit_of_work.commit()

            return box_transaction
        except Exception as e:

            self.unit_of_work.rollback()
            raise 