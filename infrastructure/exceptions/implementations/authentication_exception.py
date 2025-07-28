from infrastructure.exceptions.implementations.infraestructure_exception import InfraestructureException

class AuthenticationException(InfraestructureException):

    @staticmethod
    def invalid_credentials(property_name: str, invalid_value, message: str) -> 'AuthenticationException':
        return AuthenticationException(property_name, invalid_value, message)

    @staticmethod
    def invalid_access_token(property_name: str, invalid_value, message: str) -> 'AuthenticationException':
        return AuthenticationException(property_name, invalid_value, message)

    @staticmethod
    def invalid_refresh_token(property_name: str, invalid_value, message: str) -> 'AuthenticationException':
        return AuthenticationException(property_name, invalid_value, message)

    @staticmethod
    def expired_access_token(property_name: str, invalid_value, message: str) -> 'AuthenticationException':
        return AuthenticationException(property_name, invalid_value, message)

    @staticmethod
    def expired_refresh_token(property_name: str, invalid_value, message: str) -> 'AuthenticationException':
        return AuthenticationException(property_name, invalid_value, message)

