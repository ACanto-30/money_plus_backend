from abc import ABC, abstractmethod
from typing import Optional, Dict, Any
from domain.commands.tokens_command import TokensCommand
from domain.commands.user_login_command import UserLoginCommand

class IUserLoginService(ABC):
    """Puerto primario para el servicio de login de usuarios"""
    @abstractmethod
    def login(self, user_login_command: UserLoginCommand) -> TokensCommand:
        """Inicia sesión y retorna un diccionario con el resultado"""
        pass

    @abstractmethod
    def get_user_data(self, user_id: int) -> dict:
        """Obtiene los datos del usuario"""
        pass
