from .base_exception_handler import BaseExceptionHandler
from domain.exceptions.implementations.domain_exception import DomainException

class DomainExceptionHandler(BaseExceptionHandler):
    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, DomainException)

    def get_error_details(self, exception: Exception):
        return ("One or more validation errors occurred.", 400)

    def get_errors(self, exception: Exception):
        if hasattr(exception, "property_name"):
            return {exception.property_name: str(exception)}
        return {"Domain": str(exception)}