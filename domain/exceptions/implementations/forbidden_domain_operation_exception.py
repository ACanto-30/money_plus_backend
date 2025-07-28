from domain.exceptions.implementations.domain_exception import DomainException

class ForbiddenDomainOperationException(DomainException):
    def __init__(self, property_name: str, invalid_value: str, message: str):
        super().__init__(property_name, invalid_value, message)
        self._property_name = property_name
        self._invalid_value = invalid_value
        self._message = message

    @staticmethod
    def box_not_owner(box_id: int, user_id: int) -> 'ForbiddenDomainOperationException':
        return ForbiddenDomainOperationException("caja", box_id, f"No tienes permisos para acceder a esta caja")
