from abc import ABC, abstractmethod

class IPasswordResetService(ABC):
    """Puerto primario para el servicio de reseteo de contraseñas"""

    @abstractmethod
    def password_reset_request(self, email: str) -> bool:
        """Solicita un cambio de contraseña que genera un código de 6 digitos
        y lo envia al correo del usuario y lo guarda en la base de datos"""
        pass

    @abstractmethod
    def password_reset(self, code: int, new_password: str) -> bool:
        """Reinicia la contraseña de un usuario"""