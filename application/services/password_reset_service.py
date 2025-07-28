from domain.ports.primary.password_reset_service import IPasswordResetService
from domain.ports.secondary.password_reset_repositoy import IPasswordResetRepository
from domain.ports.secondary.unit_of_work import IUnitOfWork
from infrastructure.configuration.container import Container
from datetime import timedelta
import random
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.ports.secondary.email_sender import IEmailSender
from django.utils import timezone
from domain.ports.primary.user_service import IUserService
from domain.ports.primary.authentication_service import IAuthenticationService

class PasswordResetService(IPasswordResetService):
    """Servicio de aplicación para reseteo de contraseñas"""

    def __init__(self):
        self._password_reset_repository = Container.resolve(IPasswordResetRepository)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._email_sender = Container.resolve(IEmailSender)
        self._user_service = Container.resolve(IUserService)
        self._authentication_service = Container.resolve(IAuthenticationService)
    def password_reset_request(self, email: str) -> bool:
        """Solicita un cambio de contraseña que genera un código de 6 digitos
        y lo envia al correo del usuario y lo guarda en la base de datos"""

        try:

            # 1. INICIAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()

            user = self._user_service.get_user_by_email(email)
            if not user:
                raise InvalidDomainOperationException("Email", email, f"El usuario con email '{email}' no existe.")

            # Validar que el usuario no tenga un código de reseteo pendiente
            password_reset = self._password_reset_repository.get_code_by_user_id_and_not_expired(user.id)
            if password_reset:
                raise InvalidDomainOperationException("PasswordReset", password_reset.code, f"El usuario con email '{email}' ya tiene un código de reseteo pendiente.")

        # Generar código de 6 digitos
            code = random.randint(100000, 999999)

            # Generar fecha de expiración
            expires_at = timezone.now() + timedelta(minutes=10)

            # Guardar el código en la base de datos
            self._password_reset_repository.save_code(code, user.id, expires_at)

            # Enviar el código al correo del usuario
            self._email_sender.send_password_reset_email(email, code)

            # CONFIRMAR TRANSACCIÓN
            self._unit_of_work.commit()

        except Exception as e:
            self._unit_of_work.rollback()
            raise

        return True

    def password_reset(self, code: int, new_password: str, email: str) -> bool:
        """Reinicia la contraseña de un usuario"""

        try:
            # 1. INICIAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()

            # 2. VALIDAR QUE EL CÓDIGO DE RESETEO EXISTA, NO HAY EXPIRADO Y NO ESTE USADO
            password_reset = self._password_reset_repository.get_code(code)
            if not password_reset:
                raise InvalidDomainOperationException("Code", code, f"El código de reseteo '{code}'no es valido, ha expirado o ya ha sido usado.")

            # 3. VALIDAR QUE EL CÓDIGO DE RESETEO PERTENECE AL USUARIO
            user = self._user_service.get_user_by_email(email)
            if not user:
                raise InvalidDomainOperationException("User", email, f"El usuario con email '{email}' no existe.")

            # Validar que el id del usuario sea el mismo que el id del usuario de password_reset
            if user.id != password_reset.user_id:
                raise InvalidDomainOperationException("User", user.id, f"El usuario con id '{user.id}' no coincide con el usuario de password_reset.")

            # Hashear la nueva contraseña
            hashed_password = self._authentication_service.hash_password(new_password)

            # 4. ACTUALIZAR LA CONTRASEÑA DEL USUARIO
            self._user_service.update_password(user.id, hashed_password)

            # 5. INVALIDAR EL CÓDIGO DE RESETEO
            self._password_reset_repository.invalidate_code(code)

            # CONFIRMAR TRANSACCIÓN
            self._unit_of_work.commit()

            return True
        
        except Exception as e:
            self._unit_of_work.rollback()
            raise

    def verify_code(self, code: int) -> bool:
        """Verifica si el código de reseteo es valido"""

        try:
            # 1. INICIAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()

            # 2. VALIDAR QUE EL CÓDIGO DE RESETEO EXISTA, NO HAY EXPIRADO Y NO ESTE USADO
            password_reset = self._password_reset_repository.get_code(code)
            if not password_reset:
                raise InvalidDomainOperationException("Code", code, f"El código de reseteo '{code}'no es valido, ha expirado o ya ha sido usado.")
            
            # CONFIRMAR TRANSACCIÓN
            self._unit_of_work.commit()

            return True
        
        except Exception as e:
            self._unit_of_work.rollback()
            raise
        