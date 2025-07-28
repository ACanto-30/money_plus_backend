from abc import ABC, abstractmethod
from domain.commands.user_registration_command import UserRegistrationCommand
from domain.commands.tokens_command import TokensCommand

class IUserRegistrationService(ABC):
    """Puerto primario para el servicio de registro de usuarios"""
    
    @abstractmethod
    def register_user(self, user_registration_command: UserRegistrationCommand) -> TokensCommand:
        """Registra un usuario y genera los tokens de autenticación"""
        pass