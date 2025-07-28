from domain.exceptions.implementations.domain_exception import DomainException

class ValueObjectValidationException(DomainException):
    def __init__(self, property_name: str, invalid_value: str, message: str):
        super().__init__(property_name, invalid_value, message)
        self._property_name = property_name
        self._invalid_value = invalid_value
        self._message = message

    @staticmethod
    def invalid_email(email: str, reason: str = "Formato de email inválido") -> 'ValueObjectValidationException':
        return ValueObjectValidationException("Email", email, reason)

    @staticmethod
    def empty_or_null(property_name: str, value, reason: str = "El valor no puede ser vacío o nulo") -> 'ValueObjectValidationException':
        return ValueObjectValidationException(property_name, value, reason)