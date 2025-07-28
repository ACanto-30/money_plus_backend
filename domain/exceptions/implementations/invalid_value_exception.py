from domain.exceptions.implementations.domain_exception import DomainException

class InvalidValueException(DomainException):
    @staticmethod
    def invalid_value(property_name: str, value, reason: str = "El valor no es válido") -> 'InvalidValueException':
        return InvalidValueException(property_name, value, reason)