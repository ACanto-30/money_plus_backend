from domain.ports.secondary.saving_box_amount_box_transaction_repository import ISavingBoxAmountBoxTransactionRepository
from domain.entities.saving_box_amount_box_transaction import SavingBoxAmountBoxTransaction
from typing import Optional, List
from infrastructure.persistence.models import SavingBoxAmountBoxTransaction as SavingBoxAmountBoxTransactionModel

class SavingBoxAmountBoxTransactionRepository(ISavingBoxAmountBoxTransactionRepository):
    """Implementacion del repositorio de SavingBoxAmountBoxTransaction"""

    def save(self, saving_box_amount_box_transaction: SavingBoxAmountBoxTransaction) -> None:
        """Guarda una SavingBoxAmountBoxTransaction en la base de datos"""
        pass

    def get_by_id(self, id: int) -> Optional[SavingBoxAmountBoxTransaction]:    
        """Obtiene una SavingBoxAmountBoxTransaction por su id"""
        pass

    def get_by_saving_box_id(self, saving_box_id: int) -> List[SavingBoxAmountBoxTransaction]:
        """Obtiene todas las SavingBoxAmountBoxTransaction por el id de la caja de ahorro"""
        pass

    def get_by_amount_box_id(self, amount_box_id: int) -> List[SavingBoxAmountBoxTransaction]:
        """Obtiene todas las SavingBoxAmountBoxTransaction por el id de la caja de ahorro"""
        pass

    def get_total_amount_by_saving_box_id(self, saving_box_id: int) -> Optional[SavingBoxAmountBoxTransaction]:
        """Metodo para obtener toda la cantidad de transacciones de una caja de ahorro"""
        pass

    def get_total_amount_by_amount_box_id(self, amount_box_id: int) -> Optional[SavingBoxAmountBoxTransaction]:
        """Metodo para obtener toda la cantidad de transacciones de una caja"""
        pass

    def save_transaction(self, saving_box_amount_box_transaction: SavingBoxAmountBoxTransaction) -> bool:
        """Metodo para guardar una transaccion de la caja de ahorro a la caja amount"""
        print("Llego hasta aqui antes de guardar la transaccion")
        print("saving_box_amount_box_transaction:", saving_box_amount_box_transaction)
        print("Llego hasta aqui despues de guardar la transaccion")
        saving_box_amount_box_transaction_model = SavingBoxAmountBoxTransactionModel(
            saving_box_id=saving_box_amount_box_transaction.saving_box_id,
            amount_box_id=saving_box_amount_box_transaction.amount_box_id,
            amount=saving_box_amount_box_transaction.amount,
            transaction_type_id=saving_box_amount_box_transaction.transaction_type_id,
            created_at=saving_box_amount_box_transaction.created_at,
            updated_at=saving_box_amount_box_transaction.updated_at
        )
        print("saving_box_amount_box_transaction_model:", saving_box_amount_box_transaction_model)
        print("Llego hasta aqui despues de guardar la transaccion")
        saving_box_amount_box_transaction_model.save()
        print("Llego hasta aqui despues de guardar la transaccion")
        return True