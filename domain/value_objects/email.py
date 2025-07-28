# core/domain/value_objects/email.py
import re
from domain.exceptions.implementations.value_object_validation_exception import ValueObjectValidationException

class Email:
    """Value Object para Email - Validaciones de negocio"""
    
    def __init__(self, value: str):
        """Inicializa el Email y valida su formato"""
        if not self._verify_email(value):
            raise ValueObjectValidationException.invalid_email(value, "Invalid email format.")
        
        if value == "test@test.com":
            raise ValueObjectValidationException.invalid_email(value, "Test email is not allowed.")
        
        self._value = value
    
    def _verify_email(self, email: str) -> bool:
        """Verifica si el email tiene un formato válido"""
        try:
            pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
            return re.match(pattern, email) is not None
        except:
            return False
    
    @property
    def value(self) -> str:
        return self._value

    def __str__(self) -> str:
        return self._value