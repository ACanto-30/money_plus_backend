from abc import ABC, abstractmethod
from domain.entities.loan_repayment import LoanRepayment
from typing import List

class ILoanRepaymentRepository(ABC):
    @abstractmethod
    def get_loan_repayment_by_loan_id(self, loan_id: int) -> LoanRepayment:
        """Metodo para obtener el pago de un prestamo por el id del prestamo"""
        pass

    @abstractmethod
    def get_all_loan_repayments_by_loan_id(self, loan_id: int) -> List[LoanRepayment]:
        """Metodo para obtener todos los pagos de un prestamo por el id del prestamo"""
        pass