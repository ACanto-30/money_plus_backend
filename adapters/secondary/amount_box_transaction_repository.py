from domain.ports.secondary.amount_box_transaction_repository import IAmountBoxTransactionRepository
from domain.entities.amount_box_transaction import AmountBoxTransaction
from typing import List, Optional
from infrastructure.persistence.models import AmountBoxTransaction as AmountBoxTransactionModel
from domain.entities.amount_box import AmountBox
from infrastructure.persistence.models import AmountBox as AmountBoxModel

class AmountBoxTransactionRepository(IAmountBoxTransactionRepository):
    def make_amount_box_transaction(self, amount_box_transaction: AmountBoxTransaction) -> AmountBoxTransaction:
        """Metodo para hacer una transaccion en la caja"""
        amount_box_transaction_model = AmountBoxTransactionModel(
            id=amount_box_transaction.id,
            amount_box_id=amount_box_transaction.amount_box_id,
            amount=amount_box_transaction.amount,
            transaction_type_id=amount_box_transaction.transaction_type_id,
            created_at=amount_box_transaction.created_at,
            updated_at=amount_box_transaction.updated_at
        )
        amount_box_transaction_model.save()
        return amount_box_transaction_model.to_domain_entity()
    
    def get_amount_box_transaction_by_id(self, amount_box_transaction_id: int) -> AmountBoxTransaction:
        """Metodo para obtener una transaccion de la caja por el id"""
        amount_box_transaction_model = AmountBoxTransactionModel.objects.get(id=amount_box_transaction_id)
        return amount_box_transaction_model.to_domain_entity()
    
    def get_all_amount_box_transactions_by_amount_box_id(self, amount_box_id: int) -> List[AmountBoxTransaction]:
        """Metodo para obtener todas las transacciones de la caja por el id de la caja"""
        amount_box_transaction_models = AmountBoxTransactionModel.objects.filter(amount_box_id=amount_box_id)
        return [amount_box_transaction_model.to_domain_entity() for amount_box_transaction_model in amount_box_transaction_models]
    
    def get_sum_of_amount_box_transactions_by_amount_box_id(self, amount_box_id: int) -> Optional[AmountBoxTransaction]:
        """Metodo para obtener la suma de todas las transacciones por el id de la caja"""
        amount_box_transaction_models = AmountBoxTransactionModel.objects.filter(amount_box_id=amount_box_id)
        if not amount_box_transaction_models:
            return None
        return AmountBoxTransaction(
            id=amount_box_transaction_models[0].id,
            amount_box_id=amount_box_transaction_models[0].amount_box_id,
            amount=sum(amount_box_transaction_model.amount for amount_box_transaction_model in amount_box_transaction_models),
            created_at=amount_box_transaction_models[0].created_at,
            updated_at=amount_box_transaction_models[0].updated_at
        )

    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        """Metodo para obtener el monto de la caja de ahorro"""
        amount_box_transaction_models = AmountBoxTransactionModel.objects.filter(user_id=user_id)
        if not amount_box_transaction_models:
            return None
        return sum(amount_box_transaction_model.amount for amount_box_transaction_model in amount_box_transaction_models)

    def get_amount_box_by_user_id(self, user_id: int) -> AmountBox:
        """Metodo para obtener la caja de ahorro por el id del usuario"""
        amount_box_model = AmountBoxModel.objects.get(user_id=user_id)
        return amount_box_model.to_domain_entity()
    
    def get_all_amount_box_transactions_by_amount_box_id_and_user_id(self, amount_box_id: int, user_id: int):
        """Obtiene todas las transacciones de una caja por id de caja y usuario."""
        return AmountBoxTransactionModel.objects.filter(amount_box_id=amount_box_id, user_id=user_id)

    def get_all_amount_box_transactions_by_user_id(self, user_id: int):
        """Obtiene todas las transacciones de cajas por usuario."""
        return AmountBoxTransactionModel.objects.filter(user_id=user_id)
    