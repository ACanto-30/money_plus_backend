from abc import ABC, abstractmethod
from domain.commands.box_transfer_command import BoxTransferCommand

class IAmountBoxBoxTransactionService(ABC):
    @abstractmethod
    def make_amount_box_box_transaction(self, command: BoxTransferCommand) -> bool:
        pass