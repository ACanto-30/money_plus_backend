from .base_exception_handler import BaseExceptionHandler
from infrastructure.exceptions.implementations.authentication_exception import AuthenticationException

class AuthenticationExceptionHandler(BaseExceptionHandler):
    def can_handle(self, exception: Exception) -> bool:
        return isinstance(exception, AuthenticationException)

    def get_error_details(self, exception: Exception):
        return ("Error de autenticación", 401)

    def get_errors(self, exception: Exception):
        if hasattr(exception, "property_name"):
            return {exception.property_name: str(exception)}
        return {"Autenticación": str(exception)}