from .base_exception_handler import BaseExceptionHandler
from domain.exceptions.implementations.forbidden_domain_operation_exception import ForbiddenDomainOperationException

class ForbiddenDomainOperationExceptionHandler(BaseExceptionHandler):
    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, ForbiddenDomainOperationException)

    def get_error_details(self, exception: Exception):
        return ("Forbidden domain operation exception occurred.", 403)

    def get_errors(self, exception: Exception):
        return {"caja": str(exception)}  