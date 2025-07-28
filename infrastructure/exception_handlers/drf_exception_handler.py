from rest_framework.views import exception_handler as drf_exception_handler
from rest_framework.exceptions import ParseError
from infrastructure.exception_handlers.error_response_serializer import ProblemDetailsErrorResponseSerializer
from infrastructure.exception_handlers.domain_exception_handler import DomainExceptionHandler
from infrastructure.exception_handlers.database_exception_handler import DatabaseExceptionHandler
from infrastructure.exception_handlers.dto_exception_handler import DTOExceptionHandler
from infrastructure.exception_handlers.json_parse_exception_handler import JSONParseExceptionHandler
from infrastructure.exception_handlers.authentication_exception_handler import AuthenticationExceptionHandler
from infrastructure.exception_handlers.forbidden_domain_operation_exception_handler import ForbiddenDomainOperationExceptionHandler

def custom_exception_handler(exc, context):
    # Primero, verifica si es un error de parsing de JSON
    request = context.get('request')
    json_handler = JSONParseExceptionHandler(ProblemDetailsErrorResponseSerializer())
    
    if json_handler.can_handle(exc):
        return json_handler.handle(request, exc)
    
    # Luego, intenta el handler por defecto de DRF
    response = drf_exception_handler(exc, context)
    if response is not None:
        return response

    # Si no es manejado por DRF, usa tu lógica de Problem Details
    handlers = [
        ForbiddenDomainOperationExceptionHandler(ProblemDetailsErrorResponseSerializer()),
        DTOExceptionHandler(ProblemDetailsErrorResponseSerializer()),
        AuthenticationExceptionHandler(ProblemDetailsErrorResponseSerializer()),
        DatabaseExceptionHandler(ProblemDetailsErrorResponseSerializer()),
        DomainExceptionHandler(ProblemDetailsErrorResponseSerializer()),
        # ...otros handlers si tienes
    ]
    for handler in handlers:
        if handler.can_handle(exc):
            return handler.handle(request, exc)
    # Default: generic problem details
    serializer = ProblemDetailsErrorResponseSerializer()
    return serializer.serialize_and_send(
        request,
        errors={"General": str(exc)},
        title="One or more validation errors occurred.",
        status_code=400,
        instance=request.META.get("REQUEST_ID", request.META.get("REQUEST_TRACE_ID", ""))
    )