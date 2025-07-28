import logging
from django.db import DatabaseError, IntegrityError, OperationalError, DataError
from django.db.utils import ProgrammingError
from psycopg2 import OperationalError as Psycopg2OperationalError
from psycopg2.errors import UniqueViolation, ForeignKeyViolation, NotNullViolation, UndefinedTable, InvalidPassword, InvalidCatalogName
from .base_exception_handler import BaseExceptionHandler

class DatabaseExceptionHandler(BaseExceptionHandler):
    def __init__(self, error_response_serializer):
        super().__init__(error_response_serializer)
        self.logger = logging.getLogger(__name__)

    def can_handle(self, exception: Exception) -> bool:
        """Verifica si la excepción es una excepción de base de datos"""
        return (isinstance(exception, (DatabaseError, IntegrityError, OperationalError, DataError, ProgrammingError)) or
                isinstance(exception, Psycopg2OperationalError) or
                self._has_database_exception_in_chain(exception))

    def get_error_details(self, exception: Exception):
        """Obtiene el título y código de estado para la excepción"""
        status_code = self._get_status_code(exception)
        
        # Determinar si es un error de validación específico
        postgres_exception = self._get_postgres_exception(exception)
        if postgres_exception and hasattr(postgres_exception, 'pgcode'):
            pgcode = postgres_exception.pgcode
            if pgcode == '23505':  # unique_violation
                return ("Error de validación: Datos duplicados", 400)
            elif pgcode == '23502':  # not_null_violation
                return ("Error de validación: Campos requeridos", 400)
        
        return (self._get_title(status_code), status_code)

    def get_errors(self, exception: Exception):
        """Obtiene los errores específicos de la base de datos"""
        error_message = self._get_database_error_message(exception)
        self._log_error(exception)
        
        # Determinar el campo específico basado en el tipo de error
        postgres_exception = self._get_postgres_exception(exception)
        if postgres_exception and hasattr(postgres_exception, 'pgcode'):
            pgcode = postgres_exception.pgcode
            constraint_name = getattr(postgres_exception, 'constraint_name', '')
            error_message_text = getattr(postgres_exception, 'pgerror', str(postgres_exception))
            
            if pgcode == '23505':  # unique_violation
                if 'email' in constraint_name.lower() or 'email' in error_message_text.lower() or 'users_email_key' in constraint_name:
                    return {"email": error_message}
                elif 'username' in constraint_name.lower() or 'username' in error_message_text.lower() or 'users_username_key' in constraint_name:
                    return {"username": error_message}
                else:
                    return {"Database": error_message}
            elif pgcode == '23502':  # not_null_violation
                # Intentar extraer el nombre del campo del mensaje de error
                if 'username' in error_message_text.lower():
                    return {"username": error_message}
                elif 'email' in error_message_text.lower():
                    return {"email": error_message}
                elif 'password' in error_message_text.lower():
                    return {"password": error_message}
                else:
                    return {"Database": error_message}
        
        return {"Database": error_message}

    def _has_database_exception_in_chain(self, exception: Exception) -> bool:
        """Verifica si hay una excepción de base de datos en la cadena de excepciones"""
        current = exception
        while current is not None:
            if isinstance(current, (DatabaseError, IntegrityError, OperationalError, DataError, ProgrammingError, Psycopg2OperationalError)):
                return True
            current = getattr(current, '__cause__', None) or getattr(current, 'inner_exception', None)
        return False

    def _get_status_code(self, exception: Exception) -> int:
        """Determina el código de estado HTTP apropiado para la excepción"""
        # Verificar excepciones específicas de PostgreSQL
        postgres_exception = self._get_postgres_exception(exception)
        if postgres_exception:
            return self._get_postgres_status_code(postgres_exception)

        # Para excepciones de Django ORM
        if isinstance(exception, IntegrityError):
            return 400  # Bad Request - error de validación de datos
        if isinstance(exception, OperationalError):
            return 503  # Service Unavailable - problema de conexión
        if isinstance(exception, ProgrammingError):
            return 500  # Internal Server Error - problema de configuración
        if isinstance(exception, DataError):
            return 400  # Bad Request - error de datos

        return 503  # Service Unavailable por defecto

    def _get_postgres_status_code(self, postgres_exception) -> int:
        """Obtiene el código de estado para excepciones específicas de PostgreSQL"""
        if hasattr(postgres_exception, 'pgcode'):
            pgcode = postgres_exception.pgcode
            if pgcode in ['23505', '23503', '23502']:  # unique_violation, foreign_key_violation, not_null_violation
                return 400  # Bad Request
            elif pgcode in ['42P01', '3D000']:  # undefined_table, invalid_catalog_name
                return 500  # Internal Server Error
            elif pgcode in ['28P01', '08001']:  # invalid_password, sqlclient_unable_to_establish_sqlconnection
                return 503  # Service Unavailable

        # Verificar por tipo de excepción
        if isinstance(postgres_exception, UniqueViolation):
            return 400
        elif isinstance(postgres_exception, ForeignKeyViolation):
            return 400
        elif isinstance(postgres_exception, NotNullViolation):
            return 400
        elif isinstance(postgres_exception, UndefinedTable):
            return 500
        elif isinstance(postgres_exception, InvalidPassword):
            return 503
        elif isinstance(postgres_exception, InvalidCatalogName):
            return 500

        return 500  # Internal Server Error

    def _get_title(self, status_code: int) -> str:
        """Obtiene el título del error basado en el código de estado"""
        titles = {
            400: "Error de validación de datos",
            409: "Error de concurrencia",
            500: "Error interno del servidor",
            503: "Servicio no disponible"
        }
        return titles.get(status_code, "Error de base de datos")

    def _get_database_error_message(self, exception: Exception) -> str:
        """Obtiene el mensaje de error específico para la base de datos"""
        # Verificar excepciones específicas de PostgreSQL
        postgres_exception = self._get_postgres_exception(exception)
        if postgres_exception:
            return self._get_postgres_error_message(postgres_exception)

        # Para excepciones de Django ORM
        if isinstance(exception, IntegrityError):
            return "Error al guardar los datos en la base de datos. Verifique que los datos sean válidos."
        elif isinstance(exception, OperationalError):
            if "connection" in str(exception).lower() or "database" in str(exception).lower():
                return "No se pudo conectar a la base de datos. Verifique que el servidor esté ejecutándose."
            return "Error de operación en la base de datos."
        elif isinstance(exception, ProgrammingError):
            return "Error de configuración en la base de datos."
        elif isinstance(exception, DataError):
            return "Error en los datos proporcionados."

        return "Error inesperado en la base de datos."

    def _get_postgres_exception(self, exception: Exception):
        """Busca una excepción de PostgreSQL en la cadena de excepciones"""
        current = exception
        while current is not None:
            # Verificar si es una excepción de psycopg2
            if hasattr(current, 'pgcode') or hasattr(current, 'pgerror'):
                return current
            # Verificar tipos específicos de psycopg2
            if isinstance(current, (UniqueViolation, ForeignKeyViolation, NotNullViolation, 
                                   UndefinedTable, InvalidPassword, InvalidCatalogName)):
                return current
            current = getattr(current, '__cause__', None) or getattr(current, 'inner_exception', None)
        return None

    def _get_postgres_error_message(self, postgres_exception) -> str:
        """Obtiene mensajes de error específicos para PostgreSQL"""
        if hasattr(postgres_exception, 'pgcode'):
            pgcode = postgres_exception.pgcode
            constraint_name = getattr(postgres_exception, 'constraint_name', '')
            error_message = getattr(postgres_exception, 'pgerror', str(postgres_exception))
            
            if pgcode == '23505':  # unique_violation
                if 'username' in constraint_name.lower() or 'username' in error_message.lower():
                    return "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario."
                elif 'email' in constraint_name.lower() or 'email' in error_message.lower():
                    return "El correo electrónico ya está registrado. Por favor, use otro correo."
                elif 'users_email_key' in constraint_name:
                    return "El correo electrónico ya está registrado. Por favor, use otro correo."
                elif 'users_username_key' in constraint_name:
                    return "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario."
                return "Ya existe un registro con los mismos datos únicos."
            elif pgcode == '23503':  # foreign_key_violation
                return "Error de referencia: El registro relacionado no existe."
            elif pgcode == '23502':  # not_null_violation
                return "Error: Campo requerido sin valor."
            elif pgcode == '42P01':  # undefined_table
                return "Error: Tabla no encontrada en la base de datos."
            elif pgcode == '28P01':  # invalid_password
                return "Error de autenticación en la base de datos. Verifique las credenciales."
            elif pgcode == '3D000':  # invalid_catalog_name
                return "Error: Base de datos no encontrada."
            elif pgcode == '08001':  # sqlclient_unable_to_establish_sqlconnection
                return "No se pudo conectar a la base de datos. Verifique que el servidor esté ejecutándose."

        # Verificar por tipo de excepción
        if isinstance(postgres_exception, UniqueViolation):
            error_message = getattr(postgres_exception, 'pgerror', str(postgres_exception))
            if 'email' in error_message.lower():
                return "El correo electrónico ya está registrado. Por favor, use otro correo."
            elif 'username' in error_message.lower():
                return "El nombre de usuario ya existe. Por favor, elija otro nombre de usuario."
            return "Ya existe un registro con los mismos datos únicos."
        elif isinstance(postgres_exception, ForeignKeyViolation):
            return "Error de referencia: El registro relacionado no existe."
        elif isinstance(postgres_exception, NotNullViolation):
            return "Error: Campo requerido sin valor."
        elif isinstance(postgres_exception, UndefinedTable):
            return "Error: Tabla no encontrada en la base de datos."
        elif isinstance(postgres_exception, InvalidPassword):
            return "Error de autenticación en la base de datos. Verifique las credenciales."
        elif isinstance(postgres_exception, InvalidCatalogName):
            return "Error: Base de datos no encontrada."

        # Mensaje por defecto
        error_message = getattr(postgres_exception, 'pgerror', str(postgres_exception))
        return f"Error de base de datos: {error_message}"

    def _log_error(self, exception: Exception):
        """Registra el error en el log"""
        self.logger.error(f"Database error occurred: {str(exception)}", exc_info=True) 