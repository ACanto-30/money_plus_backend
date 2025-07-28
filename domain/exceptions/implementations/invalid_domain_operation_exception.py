from domain.exceptions.implementations.domain_exception import DomainException

class InvalidDomainOperationException(DomainException):
    @staticmethod
    def role_not_found(role_id: int) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("RoleId", role_id, f"El rol con ID '{role_id}' no existe.")

    @staticmethod
    def user_already_exists(username: str) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("Username", username, f"El usuario '{username}' ya existe.")

    @staticmethod
    def email_already_registered(email: str) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("Email", email, f"El email '{email}' ya está registrado.")

    @staticmethod
    def session_not_found(session_id: int) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("SessionId", session_id, f"La sesión con ID '{session_id}' no existe.")
    
    @staticmethod
    def session_not_found_by_uuid(uuid: str) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("Uuid", uuid, f"La sesión con UUID '{uuid}' no existe.")
    
    @staticmethod
    def session_not_found_by_refresh_token(refresh_token: str) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("RefreshToken", refresh_token, f"La sesión con Refresh Token '{refresh_token}' no existe.")
    
    @staticmethod
    def session_not_found_by_client_uuid(client_uuid: str) -> 'InvalidDomainOperationException':
        return InvalidDomainOperationException("ClientUuid", client_uuid, f"La sesión con Client UUID '{client_uuid}' no existe.")
    
    #