import logging
from pydantic import ValidationError
from .base_exception_handler import BaseExceptionHandler

class DTOExceptionHandler(BaseExceptionHandler):
    def __init__(self, error_response_serializer):
        super().__init__(error_response_serializer)
        self.logger = logging.getLogger(__name__)

    def can_handle(self, exception: Exception) -> bool:
        """Verifica si la excepción es una excepción de validación de DTO (Pydantic)"""
        return isinstance(exception, ValidationError)

    def get_error_details(self, exception: Exception):
        """Obtiene el título y código de estado para la excepción de DTO"""
        return ("Error de validación de datos", 400)

    def get_errors(self, exception: Exception):
        """Convierte los errores de Pydantic al formato Problem Details"""
        self._log_error(exception)
        
        if not isinstance(exception, ValidationError):
            return {"DTO": "Error de validación desconocido"}
        
        errors = {}
        
        # Procesar cada error de validación de Pydantic
        for error in exception.errors():
            # Obtener el campo que causó el error
            field_path = self._get_field_path(error.get('loc', []))
            
            # Obtener el mensaje de error personalizado o el original
            error_message = self._get_custom_error_message(error)
            
            # Agregar el error al diccionario
            if field_path not in errors:
                errors[field_path] = error_message
        
        return errors

    def _get_custom_error_message(self, error):
        """Obtiene el mensaje de error personalizado basado en el tipo de error"""
        error_type = error.get('type', '')
        error_message = error.get('msg', 'Error de validación')
        
        # Mapeo de tipos de error de Pydantic a mensajes en español
        error_messages = {
            'missing': 'Este campo es requerido',
            'missing_field': 'Este campo es requerido',
            'value_error.missing': 'Este campo es requerido',
            
            'string_too_short': 'Mínimo {min_length} caracteres',
            'string_too_long': 'Máximo {max_length} caracteres',
            'string_pattern_mismatch': 'Formato inválido',
            'value_error.any_str.min_length': 'Mínimo {min_length} caracteres',
            'value_error.any_str.max_length': 'Máximo {max_length} caracteres',
            'value_error.any_str.regex': 'Formato inválido',
            'value_error.str.min_length': 'Mínimo {min_length} caracteres',
            'value_error.str.max_length': 'Máximo {max_length} caracteres',
            'value_error.str.regex': 'Formato inválido',
            
            'int_parsing': 'Debe ser un número entero válido',
            'float_parsing': 'Debe ser un número decimal válido',
            'bool_parsing': 'Debe ser verdadero o falso',
            
            'value_error.email': 'Formato de email inválido',
            'value_error.url': 'Formato de URL inválido',
            
            'value_error.number.not_gt': 'Debe ser mayor que {limit_value}',
            'value_error.number.not_ge': 'Debe ser mayor o igual a {limit_value}',
            'value_error.number.not_lt': 'Debe ser menor que {limit_value}',
            'value_error.number.not_le': 'Debe ser menor o igual a {limit_value}',
            
            'greater_than': 'Debe ser mayor que {gt}',
            'less_than': 'Debe ser menor que {lt}',
            'greater_than_equal': 'Debe ser mayor o igual a {ge}',
            'less_than_equal': 'Debe ser menor o igual a {le}',
        }
        
        # Buscar un mensaje personalizado para el tipo de error
        if error_type in error_messages:
            custom_message = error_messages[error_type]
            
            # Reemplazar placeholders con valores del contexto
            ctx = error.get('ctx', {})
            for key, value in ctx.items():
                placeholder = f"{{{key}}}"
                if placeholder in custom_message:
                    custom_message = custom_message.replace(placeholder, str(value))
            
            return custom_message
        
        # Si no hay mensaje personalizado, usar el original
        return error_message

    def _get_field_path(self, location):
        """Convierte la ubicación del error de Pydantic a un nombre de campo legible"""
        if not location:
            return "unknown"
        
        # Convertir la lista de ubicaciones a un string
        return ".".join(str(loc) for loc in location)

    def _log_error(self, exception: Exception):
        """Registra el error en el log"""
        if isinstance(exception, ValidationError):
            self.logger.warning(f"DTO validation error: {len(exception.errors())} validation errors found")
            for error in exception.errors():
                field_path = self._get_field_path(error.get('loc', []))
                error_type = error.get('type', 'unknown')
                error_message = error.get('msg', 'unknown error')
                self.logger.debug(f"  Field: {field_path}, Type: {error_type}, Message: {error_message}")
        else:
            self.logger.error(f"DTO error occurred: {str(exception)}", exc_info=True) 