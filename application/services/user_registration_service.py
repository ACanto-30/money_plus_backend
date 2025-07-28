from typing import Dict, Any
from domain.entities.user import User as UserEntity
from domain.entities.role import Role as RoleEntity
from domain.value_objects.email import Email
from domain.ports.secondary.user_repository import IUserRepository
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.ports.primary.user_registratation_service import IUserRegistrationService
from domain.ports.primary.authentication_service import IAuthenticationService
from domain.ports.primary.session_service import ISessionService
from domain.exceptions.implementations import InvalidDomainOperationException
from infrastructure.configuration.container import Container
import logging
from datetime import timedelta
from domain.commands.user_registration_command import UserRegistrationCommand
from domain.commands.tokens_command import TokensCommand
from domain.commands.access_token_payload_command import AccessTokenPayloadCommand
from domain.commands.session_command import SessionCommand
from django.utils import timezone
from domain.ports.primary.role_service import IRoleService
from domain.entities.saving_box import SavingBox
from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.entities.amount_box import AmountBox

logger = logging.getLogger(__name__)

class UserRegistrationService(IUserRegistrationService):
    """
    Servicio de aplicación para registro de usuarios
    
    Este servicio implementa el patrón Unit of Work para garantizar
    que todas las operaciones de registro se ejecuten como una sola
    transacción atómica.
    """
    
    def __init__(self):
        # Inyección de dependencias usando el Container
        self._user_repository = Container.resolve(IUserRepository)
        self._role_service = Container.resolve(IRoleService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._authentication_service = Container.resolve(IAuthenticationService)
        self._session_service = Container.resolve(ISessionService)
        self._saving_box_service = Container.resolve(ISavingBoxService)
        self._amount_box_service = Container.resolve(IAmountBoxService)

    def register_user(self, user_registration_command: UserRegistrationCommand) -> TokensCommand:
        """
        Registra un usuario usando Unit of Work para transacciones atómicas
        y genera los tokens de autenticación
        
        Args:
            payload: Diccionario con los datos del usuario
            
        Returns:
            Dict[str, Any]: Diccionario con access_token y refresh_token
            
        Raises:
            InvalidDomainOperationException: Si el rol no existe
            Exception: Si hay error en la transacción
        """
        logger.info(f"Iniciando registro de usuario: {user_registration_command.username}")
        
        try:
            # 1. INICIAR TRANSACCIÓN
            # El Unit of Work inicia una transacción PostgreSQL
            # BEGIN TRANSACTION;
            self._unit_of_work.begin_transaction()
            logger.debug("Transacción iniciada")
            
            # 2. VALIDAR QUE EL ROL EXISTE
            # Usamos el repositorio en lugar de acceder directamente a la BD
            role_entity = self._role_service.get_role_by_id(user_registration_command.role_id)
            if not role_entity:
                logger.warning(f"Rol no encontrado: {user_registration_command.role_id}")
                raise InvalidDomainOperationException.role_not_found(user_registration_command.role_id)
            
            if role_entity.name != "user":
                raise InvalidDomainOperationException("Role", user_registration_command.role_id, "El rol no es valido")

            logger.debug(f"Rol validado: {role_entity.name}")
            
            # 3. CREAR ENTIDAD DE USUARIO
            # Validación de dominio usando Value Objects
            email_vo = Email(user_registration_command.email)
            
            # Hash de contraseña usando el servicio de autenticación
            hashed_password = self._authentication_service.hash_password(user_registration_command.password)
            
            # Crear entidad de dominio
            user_entity = UserEntity(
                username=user_registration_command.username,
                password=hashed_password,
                email=email_vo,
                role_id=user_registration_command.role_id
            )

            logger.debug("Entidad de usuario creada")
            
            # 4. GUARDAR USUARIO
            # El repositorio usa la transacción activa del Unit of Work
            print("Llego hasta aqui antes de guardar el usuario")
            print("user_entity:", user_entity)
            user_id = self._user_repository.save(user_entity)
            
            logger.debug(f"Usuario guardado con ID: {user_id}")

            # 5. GENERAR TOKENS DENTRO DE LA TRANSACCIÓN
            
            # Crear el payload para el token de acceso
            access_token_payload = AccessTokenPayloadCommand(
                user_id=user_id,
                username=user_registration_command.username,
                email=user_registration_command.email,
                role_id=user_registration_command.role_id,
                client_uuid=user_registration_command.client_uuid
            )
            
            # Token de acceso
            access_token = self._authentication_service.generate_access_token(access_token_payload, 3600)
            
            logger.debug("Tokens generados exitosamente")

            # Token de refresco
            refresh_token = self._authentication_service.generate_refresh_token(user_id)
            
            token_created_at = timezone.now()
            # Definir fecha de expiracion del token
            expires_at = token_created_at + timedelta(days=30)

            # 6. CREAR LA SESION
            session_command = SessionCommand(
                user_id=user_id,
                refresh_token=refresh_token,
                client_uuid=user_registration_command.client_uuid,
                token_created_at=token_created_at,
                expires_at=expires_at
            )

            # Crear la sesión
            self._session_service.create_session(session_command)

            print("Llego hasta aqui antes de crear la caja de ahorro")
            # Crear la caja de ahorro
            saving_box = SavingBox(
                user_id=user_id,
                amount=0,
            )
            print("Llego hasta aqui antes de crear la caja de ahorro")
            self._saving_box_service.create_saving_box(saving_box)
            print("Llego hasta aqui despues de crear la caja de ahorro")
            # Crear amount box
            amount_box = AmountBox(
                user_id=user_id,
                amount=0,
            )
            print("Llego hasta aqui antes de crear la caja amount") 
            self._amount_box_service.create_amount_box(amount_box)
            print("Llego hasta aqui despues de crear la caja amount")

            # 7. CONFIRMAR TRANSACCIÓN
            # COMMIT; - Todos los cambios se confirman juntos
            self._unit_of_work.commit()
            
            logger.info(f"Usuario registrado exitosamente: {user_registration_command.username} (ID: {user_id})")
            
            # 8. DEVOLVER TOKENS
            return TokensCommand(access_token=access_token, refresh_token=refresh_token)
            
        except Exception as e:
            # 9. ROLLBACK EN CASO DE ERROR DE DOMINIO
            # ROLLBACK; - Se revierten todos los cambios
            logger.error(f"Error de dominio en registro de usuario: {user_registration_command.username}")
            logger.error(f"Haciendo rollback")
            self._unit_of_work.rollback()
            raise
            