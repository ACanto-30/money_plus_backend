from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.entities.saving_box import SavingBox
from infrastructure.configuration.container import Container
from domain.ports.secondary.saving_box_repository import ISavingBoxRepository
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from domain.entities.saving_box import SavingBox

class SavingBoxService(ISavingBoxService):
    def __init__(self):
        self._saving_box_repository = Container.resolve(ISavingBoxRepository)

    def get_saving_box_by_id(self, saving_box_id: int) -> SavingBox:
        """Metodo para obtener una caja de ahorro por su id"""
        # Como no hay get_saving_box_by_id en la interfaz, necesitamos implementar esto de otra manera
        # Por ahora, vamos a buscar por user_id asumiendo que saving_box_id es el user_id
        saving_box = self._saving_box_repository.get_saving_box_by_id(saving_box_id)
        if not saving_box:
            raise InvalidDomainOperationException("caja de ahorro", saving_box_id, "La caja de ahorro no existe")
        return saving_box

    def get_saving_box_by_user_id(self, user_id: int) -> SavingBox:
        """Metodo para obtener una caja de ahorro por el id del usuario"""
        saving_box = self._saving_box_repository.get_saving_box_by_user_id(user_id)
        if not saving_box:
            raise InvalidDomainOperationException("caja de ahorro", user_id, "La caja de ahorro no existe")
        return saving_box

    def make_saving_box_transaction(self, saving_box: SavingBox) -> bool:
        """Metodo para hacer una transaccion de la caja de ahorro"""
        # NO EMPEZAMOS UNA TRANSACCIÓN, PORQUE SOLO SE HACE UNA TRANSACCIÓN POR CAJA

         # SOLO SE ACTUALIZA EL AMOUNT DE LA CAJA
        # Guardamos la caja de ahorro
        self._saving_box_repository.update_saving_box(saving_box)

        return True

    def create_saving_box(self, saving_box: SavingBox) -> bool:
        """Metodo para crear una caja de ahorro"""
        self._saving_box_repository.create_saving_box(saving_box)

        return True

    def get_total_amount_box_by_user_id(self, user_id: int) -> int:
        saving_box = self._saving_box_repository.get_saving_box_by_user_id(user_id)
        if not saving_box:
            raise InvalidDomainOperationException("caja de ahorro", user_id, "La caja de ahorro no existe")
        return saving_box.amount

