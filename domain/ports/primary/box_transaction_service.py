from abc import ABC, abstractmethod
from domain.commands.box_transaction_command import BoxTransactionCommand

class IBoxTransactionService(ABC):
    @abstractmethod
    def make_box_transaction(self, command: BoxTransactionCommand) -> bool:
        """Metodo para hacer una transaccion de la caja"""
        pass