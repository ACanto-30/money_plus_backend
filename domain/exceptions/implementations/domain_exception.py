from domain.exceptions.interfaces.domain_exception import IDomainException

class DomainException(Exception, IDomainException):
    def __init__(self, property_name: str, invalid_value, message: str):
        super().__init__(message)
        self._property_name = property_name
        self._invalid_value = invalid_value
        self._message = message

    @property
    def property_name(self) -> str:
        return self._property_name

    @property
    def invalid_value(self):
        return self._invalid_value

    @property
    def message(self) -> str:
        return self._message

    def __str__(self) -> str:
        return self._message