from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.secondary.amount_box_repository import IAmountBoxRepository
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.entities.amount_box import AmountBox
from domain.exceptions.implementations import InvalidDomainOperationException
from infrastructure.configuration.container import Container

class AmountBoxService(IAmountBoxService):
    def __init__(self):
        self._amount_box_repository = Container.resolve(IAmountBoxRepository)

    def get_amount_box_by_id(self, amount_box_id: int) -> AmountBox:
        # Como no hay get_amount_box_by_id en la interfaz, necesitamos implementar esto de otra manera
        # Por ahora, vamos a buscar por user_id asumiendo que amount_box_id es el user_id
        amount_box = self._amount_box_repository.get_amount_box_by_id(amount_box_id)
        print("amount_box:", amount_box, type(amount_box))
        if not amount_box:
            raise InvalidDomainOperationException("amount_box", amount_box_id, "El amount_box no existe")
        return amount_box

    def get_amount_box_by_user_id(self, user_id: int) -> AmountBox:
        amount_box = self._amount_box_repository.get_amount_box_by_user_id(user_id)
        if not amount_box:
            raise InvalidDomainOperationException("amount_box", user_id, "El amount_box no existe")
        return amount_box

    def make_amount_box_transaction(self, amount_box: AmountBox) -> bool:
        # NO EMPEZAMOS UNA TRANSACCIÓN, PORQUE SOLO SE HACE UNA TRANSACCIÓN POR CAJA
      
        # SOLO SE ACTUALIZA EL AMOUNT DE LA CAJA

        self._amount_box_repository.make_amount_box_transaction(amount_box)

        return True

    def create_amount_box(self, amount_box: AmountBox) -> bool:
        # Usar el método create_amount_box del repositorio
        print("Llego hasta aqui antes de crear la caja amount")
        print("amount_box:", amount_box)
        self._amount_box_repository.create_amount_box(amount_box)

        return True
    
    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        print("Entro al get_total_amount_box_by_user_id")
        print(user_id)
        amount_box = self._amount_box_repository.get_amount_box_by_user_id(user_id)
        if not amount_box:
            raise InvalidDomainOperationException("amount_box", user_id, "El amount_box no existe")
        return amount_box.amount