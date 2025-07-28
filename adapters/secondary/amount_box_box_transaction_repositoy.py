from domain.ports.secondary.amount_box_box_transaction_repository import IAmountBoxBoxTransactionRepository
from domain.entities.amount_box_box_transaction import AmountBoxBoxTransaction
from typing import List, Optional
from infrastructure.persistence.models import AmountBoxBoxTransaction as AmountBoxBoxTransactionModel

class AmountBoxBoxTransactionRepository(IAmountBoxBoxTransactionRepository):

    def save(self, amount_box_box_transaction: AmountBoxBoxTransaction) -> AmountBoxBoxTransaction:
        """Metodo para guardar la transaccion de la caja"""
        amount_box_box_transaction_model = AmountBoxBoxTransactionModel.from_domain_entity(amount_box_box_transaction)
        amount_box_box_transaction_model.save()
        return amount_box_box_transaction_model.to_domain_entity()

    def get_amount_box_box_transaction_by_id(self, amount_box_box_transaction_id: int) -> AmountBoxBoxTransaction:
        """Metodo para obtener la transaccion de la caja por el id"""
        amount_box_box_transaction_model = AmountBoxBoxTransactionModel.objects.get(id=amount_box_box_transaction_id)
        return amount_box_box_transaction_model.to_domain_entity()
    
    def make_amount_box_box_transaction(self, amount_box_box_transaction: AmountBoxBoxTransaction) -> AmountBoxBoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        amount_box_box_transaction_model = AmountBoxBoxTransactionModel(
            id=amount_box_box_transaction.id,
            amount_box_id=amount_box_box_transaction.amount_box_id,
            amount=amount_box_box_transaction.amount,
            created_at=amount_box_box_transaction.created_at,
            updated_at=amount_box_box_transaction.updated_at
        )
        amount_box_box_transaction_model.save()
        return amount_box_box_transaction_model.to_domain_entity()
    
    def get_all_amount_box_box_transactions_by_amount_box_id(self, amount_box_id: int) -> List[AmountBoxBoxTransaction]:
        """Metodo para obtener todas las transacciones de la caja por el id de la caja"""
        amount_box_box_transaction_models = AmountBoxBoxTransactionModel.objects.filter(amount_box_id=amount_box_id)
        return [amount_box_box_transaction_model.to_domain_entity() for amount_box_box_transaction_model in amount_box_box_transaction_models]
    
    def get_sum_of_amount_box_box_transactions_by_amount_box_id(self, amount_box_id: int) -> Optional[AmountBoxBoxTransaction]:
        """Metodo para obtener la suma de todas las transacciones por el id del amount_box
        retornara la entity de AmountBoxBoxTransaction, pero el amount sera la suma de todas las transacciones de la caja"""
        amount_box_box_transaction_models = AmountBoxBoxTransactionModel.objects.filter(amount_box_id=amount_box_id)

        if not amount_box_box_transaction_models:
            return None

        return AmountBoxBoxTransaction(
            id=amount_box_box_transaction_models[0].id,
            amount_box_id=amount_box_box_transaction_models[0].amount_box_id,
            amount=sum(amount_box_box_transaction_model.amount for amount_box_box_transaction_model in amount_box_box_transaction_models),
            created_at=amount_box_box_transaction_models[0].created_at,
            updated_at=amount_box_box_transaction_models[0].updated_at,
        )

    