from .interfaces import ICustomExceptionHandler

class BaseExceptionHandler(ICustomExceptionHandler):
    def __init__(self, error_response_serializer):
        self.error_response_serializer = error_response_serializer

    def can_handle(self, exception: Exception) -> bool:
        raise NotImplementedError

    def handle(self, request, exception: Exception):
        title, status_code = self.get_error_details(exception)
        errors = self.get_errors(exception)
        instance = request.get_full_path() if hasattr(request, "get_full_path") else ""
        return self.error_response_serializer.serialize_and_send(
            request, errors, title, status_code, instance
        )

    def get_error_details(self, exception: Exception):
        raise NotImplementedError

    def get_errors(self, exception: Exception):
        raise NotImplementedError