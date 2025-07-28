from domain.ports.primary.transaction_type_service import ITransactionTypeService
from domain.ports.secondary.transaction_type_repository import ITransactionTypeRepository
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.entities.transaction_type import TransactionType
from infrastructure.configuration.container import Container

class TransactionTypeService(ITransactionTypeService):
    def __init__(self):
        self._transaction_type_repository = Container.resolve(ITransactionTypeRepository)

    def get_transaction_type_by_id(self, transaction_type_id: int) -> TransactionType:
        print("transaction_type_id:", transaction_type_id)
        transaction_type = self._transaction_type_repository.get_transaction_type_by_id(transaction_type_id)
        if not transaction_type:
            raise InvalidDomainOperationException("transaccion", transaction_type_id, "El tipo de transaccion no existe")
        return transaction_type