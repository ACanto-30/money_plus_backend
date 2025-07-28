import logging
import json
from rest_framework.parsers import JSONParser
from rest_framework.exceptions import ParseError
from .base_exception_handler import BaseExceptionHandler

class JSONParseExceptionHandler(BaseExceptionHandler):
    def __init__(self, error_response_serializer):
        super().__init__(error_response_serializer)
        self.logger = logging.getLogger(__name__)

    def can_handle(self, exception: Exception) -> bool:
        """Verifica si la excepción es un error de parsing de JSON"""
        return isinstance(exception, ParseError) or self._is_json_parse_error(exception)

    def get_error_details(self, exception: Exception):
        """Obtiene el título y código de estado para la excepción de parsing de JSON"""
        return ("Formato de solicitud inválido", 400)

    def get_errors(self, exception: Exception):
        """Convierte los errores de parsing de JSON al formato Problem Details"""
        self._log_error(exception)
        
        error_message = self._get_json_error_message(exception)
        return {"JSON": error_message}

    def _is_json_parse_error(self, exception: Exception) -> bool:
        """Verifica si la excepción es un error de parsing de JSON"""
        error_message = str(exception).lower()
        json_error_indicators = [
            'json parse error',
            'expecting property name',
            'unexpected token',
            'unterminated string',
            'invalid json',
            'jsondecodeerror',
            'json.decoder.jsondecodeerror'
        ]
        
        return any(indicator in error_message for indicator in json_error_indicators)

    def _get_json_error_message(self, exception: Exception) -> str:
        """Obtiene un mensaje de error descriptivo para errores de JSON"""
        error_message = str(exception).lower()
        
        # Mapeo de errores comunes de JSON a mensajes en español
        if 'expecting property name' in error_message:
            return "Formato JSON inválido: verifique que las propiedades estén correctamente cerradas"
        elif 'unterminated string' in error_message:
            return "Formato JSON inválido: cadena de texto no cerrada correctamente"
        elif 'unexpected token' in error_message:
            return "Formato JSON inválido: token inesperado en la estructura"
        elif 'trailing comma' in error_message or 'comma' in error_message:
            return "Formato JSON inválido: coma extra al final de una lista u objeto"
        elif 'missing' in error_message and 'quote' in error_message:
            return "Formato JSON inválido: comillas faltantes en nombres de propiedades"
        elif 'invalid json' in error_message:
            return "Formato JSON inválido: estructura de datos incorrecta"
        elif 'json parse error' in error_message:
            return "Formato JSON inválido: error al procesar la solicitud"
        else:
            return "Formato de solicitud inválido: verifique que el JSON esté correctamente formateado"

    def _log_error(self, exception: Exception):
        """Registra el error en el log"""
        self.logger.warning(f"JSON parse error: {str(exception)}")
        self.logger.debug(f"Exception type: {type(exception).__name__}") 