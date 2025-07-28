from abc import ABC, abstractmethod
from domain.commands.box_transfer_command import BoxTransferCommand

class ISavingBoxBoxTransactionService(ABC):
    @abstractmethod
    def make_saving_box_box_transaction(self, command: BoxTransferCommand) -> bool:
        """Metodo para hacer una transaccion de la caja de ahorro"""
        pass

    