from abc import ABC, abstractmethod
from domain.entities.loan_state import LoanState
from typing import List

class ILoanStateRepository(ABC):
    @abstractmethod
    def get_loan_state_by_id(self, loan_state_id: int) -> LoanState:
        """Metodo para obtener el estado de un prestamo por el id"""
        pass

    @