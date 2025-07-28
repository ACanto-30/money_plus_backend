from abc import ABC, abstractmethod
from typing import List, Dict, Any
from domain.commands.email_command import EmailCommand

class IEmailSender(ABC):
    """Puerto secundario para el servicio de envío de emails"""
    
    @abstractmethod
    def send_email(self, email_command: EmailCommand) -> bool:
        """
        Envía un email

        Args:
            email_command: EmailCommand con los datos del email
            
        Returns:
            True si el email se envió correctamente, False en caso contrario
        """
        pass
    
    @abstractmethod
    def send_bulk_email(self, emails_data: List[EmailCommand]) -> bool:
        """
        Envía múltiples emails
        
        Args:
            emails_data: Lista de EmailCommand con los datos de los emails
                        
        Returns:
            Lista de dicts con keys: success (bool), message_id (str), error_message (str)
        """
        pass
    
    @abstractmethod
    def test_connection(self) -> bool:
        """
        Prueba la conexión con el servidor de email
        
        Returns:
            True si la conexión es exitosa, False en caso contrario
        """
        pass
    
    @abstractmethod
    def send_password_reset_email(self, to_email: str, code: int) -> bool:
        """
        Envía un email de reseteo de contraseña
        
        Args:
            to_email: Email del destinatario
            code: Código de reseteo de 6 dígitos
            
        Returns:
            True si el email se envió correctamente, False en caso contrario
        """
        pass 