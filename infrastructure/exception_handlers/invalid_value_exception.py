from infrastructure.exception_handlers.base_exception_handler import BaseExceptionHandler
from domain.exceptions.implementations.invalid_value_exception import InvalidValueException

class InvalidValueExceptionHandler(BaseExceptionHandler):
    def __init__(self, error_response_serializer):
        super().__init__(error_response_serializer)

    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, InvalidValueException)

    def get_error_details(self, exception: Exception):
        return ("Error de validación de datos", 400)