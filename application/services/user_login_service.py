from domain.ports.secondary.user_repository import IUserRepository
from domain.ports.primary.session_service import ISessionService
from domain.ports.primary.user_login_service import IUserLoginService
from domain.ports.secondary.unit_of_work import IUnitOfWork
from infrastructure.configuration.container import Container
from domain.commands.user_login_command import UserLoginCommand
from domain.commands.tokens_command import TokensCommand
from domain.ports.primary.authentication_service import IAuthenticationService
from domain.commands.access_token_payload_command import AccessTokenPayloadCommand
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.commands.session_command import SessionCommand
import logging
from datetime import datetime

logger = logging.getLogger(__name__)

class UserLoginService(IUserLoginService):
    """Servicio de aplicación para login de usuarios"""
    
    def __init__(self):
        self._user_repository = Container.resolve(IUserRepository)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._authentication_service = Container.resolve(IAuthenticationService)
        self._session_service = Container.resolve(ISessionService)

    def login(self, user_login_command: UserLoginCommand) -> TokensCommand:
        """Inicia sesión y retorna un diccionario con el resultado"""

        logger.info(f"Iniciando login de usuario: {user_login_command.email}")

        try:
            # 1. INICIAR TRANSACCIÓN
            self._unit_of_work.begin_transaction()
            logger.debug("Transacción iniciada")

            # 2. VALIDAR QUE EL USUARIO EXISTE
            user = self._user_repository.get_by_email(user_login_command.email)
            if not user:
                raise InvalidDomainOperationException("Email", user_login_command.email, f"El usuario con email '{user_login_command.email}' no existe.")

            # 3. VALIDAR QUE LA CONTRASEÑA SEA CORRECTA
            if not self._authentication_service.verify_password(user_login_command.password, user.password):
                raise InvalidDomainOperationException("Password", user_login_command.password, f"Contraseña incorrecta para el email '{user_login_command.email}'.")

            print("Llego hasta aqui antes de verificar si ya tiene una sesion activa con el mismo client_uuid")
            # 4. VERIFICAR SI YA TIENE UNA SESION ACTIVA CON EL MISMO CLIENT_UUID
            session = self._session_service.get_session_by_client_uuid(user_login_command.client_uuid)
            if session:
                print("Llego hasta aqui antes de generar el payload de token de acceso")
                # Generamos un nuevo token de acceso
                access_token_payload = AccessTokenPayloadCommand(
                    user_id=user.id,
                    username=user.username,
                    email=str(user.email),
                    role_id=user.role_id,
                    client_uuid=user_login_command.client_uuid
                )
                print("access_token_payload:", access_token_payload)
                logger.debug("Payload de token de acceso generado")

                access_token = self._authentication_service.generate_access_token(access_token_payload, 3600)

                logger.debug("Token de acceso generado")

                # 5. CONFIRMAR TRANSACCIÓN
                self._unit_of_work.commit()

                logger.debug("Transacción confirmada")

                return TokensCommand(access_token=access_token, refresh_token=session.refresh_token)


            # 4. GENERAR TOKENS

            print("Llego hasta aqui antes de generar el token de refresco")
            refresh_token = self._authentication_service.generate_refresh_token(user.id)
            print("refresh_token:", refresh_token)

            print("Llego hasta aqui antes de generar el payload de token de acceso")
            # 5. GENERAR TOKEN DE ACCESO
            access_token_payload = AccessTokenPayloadCommand(
                user_id=user.id,
                username=user.username,
                email=str(user.email),
                role_id=user.role_id,
                client_uuid=user_login_command.client_uuid
            )
            print("access_token_payload:", access_token_payload)
            logger.debug("Payload de token de acceso generado")

            access_token = self._authentication_service.generate_access_token(access_token_payload, 3600)

            logger.debug("Token de acceso generado")

            # DECODIFICAR TOKEN DE REFRESCO
            decoded_token = self._authentication_service.decode_refresh_token(refresh_token)

            logger.debug("Token de refresco decodificado")

            # Convertir timestamps a datetime
            token_created_at = datetime.fromtimestamp(decoded_token.iat)
            expires_at = datetime.fromtimestamp(decoded_token.exp)

            print("token_created_at:", token_created_at)
            print("expires_at:", expires_at)

            # 5. CREAR LA SESION
            session_command = SessionCommand(
                user_id=user.id,
                refresh_token=refresh_token,
                client_uuid=user_login_command.client_uuid,
                token_created_at=token_created_at,
                expires_at=expires_at,
            )
            print("session_command:", session_command)
            logger.debug("Sesión creada")

            # 6. Guardar la sesión usando el session_service
            self._session_service.create_session(session_command)
            print("session_command despues de guardar la sesion")
            logger.debug("Sesión guardada")

            # 7. CONFIRMAR TRANSACCIÓN
            self._unit_of_work.commit()

            logger.debug("Transacción confirmada")

            return TokensCommand(access_token=access_token, refresh_token=refresh_token)
            
        except Exception as e:
            logger.error(f"Error de dominio en login de usuario: {user_login_command.email}")
            logger.error(f"Haciendo rollback")
            self._unit_of_work.rollback()
            raise

    def get_user_data(self, user_id: int) -> dict:
        """Obtiene el username y email de un usuario por su id."""
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise InvalidDomainOperationException("User", user_id, f"El usuario con id '{user_id}' no existe.")
        return {
            'username': user.username,
            'email': user.email.value if hasattr(user.email, 'value') else str(user.email)
        }
