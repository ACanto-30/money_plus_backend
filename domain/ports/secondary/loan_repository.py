from abc import ABC, abstractmethod
from domain.entities.loan import Loan
from typing import List

class ILoanRepository(ABC):
    @abstractmethod
    def get_loan_by_user_id(self, user_id: int) -> Loan:
        """Metodo para obtener el prestamo por el id del usuario"""
        pass

    @abstractmethod
    def get_all_loans_by_user_id(self, user_id: int) -> List[Loan]:
        """Metodo para obtener todos los prestamos por el id del usuario"""
        pass

    @abstractmethod
    def create_loan(self, loan: Loan) -> Loan:
        """Metodo para crear un prestamo"""
        pass
