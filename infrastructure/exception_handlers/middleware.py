from django.utils.deprecation import MiddlewareMixin
from .error_response_serializer import ProblemDetailsErrorResponseSerializer
from .domain_exception_handler import DomainExceptionHandler
from .database_exception_handler import DatabaseExceptionHandler
from .invalid_value_exception import InvalidValueExceptionHandler

class GlobalExceptionMiddleware(MiddlewareMixin):
    def __init__(self, get_response):
        self.get_response = get_response
        self.handlers = [
            DomainExceptionHandler(ProblemDetailsErrorResponseSerializer()),
            DatabaseExceptionHandler(ProblemDetailsErrorResponseSerializer()),
            InvalidValueExceptionHandler(ProblemDetailsErrorResponseSerializer()),
            # Puedes agregar más handlers aquí
        ]

    def __call__(self, request):
        try:
            response = self.get_response(request)
            return response
        except Exception as ex:
            for handler in self.handlers:
                if handler.can_handle(ex):
                    return handler.handle(request, ex)
            # Default: generic problem details
            serializer = ProblemDetailsErrorResponseSerializer()
            return serializer.serialize_and_send(
                request,
                errors={"General": str(ex)},
                title="One or more validation errors occurred.",
                status_code=400,
                instance=request.META.get("REQUEST_ID", request.META.get("REQUEST_TRACE_ID", ""))
            )