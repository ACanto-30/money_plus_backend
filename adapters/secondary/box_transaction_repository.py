from domain.ports.secondary.box_transaction_repository import IBoxTransactionRepository
from domain.entities.box_transaction import BoxTransaction
from infrastructure.persistence.models import BoxTransaction

class BoxTransactionRepository(IBoxTransactionRepository):
    def make_box_transaction(self, box_transaction: BoxTransaction) -> BoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        box_transaction_model = BoxTransaction.objects.create(
            box_id=box_transaction.box_id,
            amount=box_transaction.amount,
            transaction_type_id=box_transaction.transaction_type_id,
            created_at=box_transaction.created_at,
            updated_at=box_transaction.updated_at
        )
        return box_transaction_model.to_domain_entity()