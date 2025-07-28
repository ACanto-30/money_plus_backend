from domain.ports.secondary.transaction_type_repository import ITransactionTypeRepository
from domain.entities.transaction_type import TransactionType
from typing import List
from infrastructure.persistence.models import TransactionType as TransactionTypeModel
from domain.exceptions.implementations import InvalidDomainOperationException

class TransactionTypeRepository(ITransactionTypeRepository):
    """Implementacion del repositorio de TransactionType"""

    def get_transaction_type_by_id(self, transaction_type_id: int) -> TransactionType:
        """Metodo para obtener el tipo de transaccion por el id"""
        print("transaction_type_id:", transaction_type_id)
        transaction_type = TransactionTypeModel.objects.get(id=transaction_type_id)
        return transaction_type.to_domain_entity()

    def get_all_transaction_types(self) -> List[TransactionType]:
        """Metodo para obtener todos los tipos de transaccion"""
        transaction_types = TransactionTypeModel.objects.all()
        return [transaction_type.to_domain_entity() for transaction_type in transaction_types]