from domain.ports.secondary.saving_box_box_transaction_repository import ISavingBoxBoxTransactionRepository
from domain.entities.saving_box_box_transaction import SavingBoxBoxTransaction
from typing import Optional, List
from infrastructure.persistence.models import SavingBoxBoxTransaction as SavingBoxBoxTransactionModel
from domain.exceptions.implementations import InvalidDomainOperationException

class SavingBoxBoxTransactionRepository(ISavingBoxBoxTransactionRepository):
    """Implementacion del repositorio de SavingBoxBoxTransaction"""

    def save(self, saving_box_box_transaction: SavingBoxBoxTransaction) -> SavingBoxBoxTransaction:
        """Guarda una SavingBoxBoxTransaction en la base de datos"""
        # Obtener modelo por id
        saving_box_box_transaction_model = SavingBoxBoxTransactionModel(
            saving_box_id=saving_box_box_transaction.saving_box_id,
            box_id=saving_box_box_transaction.box_id,
            amount=saving_box_box_transaction.amount,
            transaction_type_id=saving_box_box_transaction.transaction_type_id,
            created_at=saving_box_box_transaction.created_at,
            updated_at=saving_box_box_transaction.updated_at
        )
        saving_box_box_transaction_model.save()
        return saving_box_box_transaction_model.to_domain_entity()
        
    def get_by_id(self, id: int) -> Optional[SavingBoxBoxTransaction]:
        """Obtiene una SavingBoxBoxTransaction por su id"""
        saving_box_box_transaction_model = SavingBoxBoxTransactionModel.objects.get(id=id)
        if saving_box_box_transaction_model is None:
            raise InvalidDomainOperationException("saving_box_box_transaction", id, "SavingBoxBoxTransaction no existe")
        return saving_box_box_transaction_model.to_domain_entity()



