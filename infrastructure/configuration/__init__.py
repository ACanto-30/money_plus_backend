# Primero importamos las interfaces
from domain.ports.secondary.user_repository import IUserRepository
from domain.ports.secondary.role_repository import IRoleRepository
from domain.ports.secondary.session_repository import ISessionRepository
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.ports.secondary.email_sender import IEmailSender
from domain.ports.secondary.password_reset_repositoy import IPasswordResetRepository
from domain.ports.primary.user_registratation_service import IUserRegistrationService
from domain.ports.primary.authentication_service import IAuthenticationService
from domain.ports.primary.session_service import ISessionService
from domain.ports.primary.user_login_service import IUserLoginService
from domain.ports.primary.password_reset_service import IPasswordResetService
from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from domain.ports.secondary.saving_box_repository import ISavingBoxRepository
from domain.ports.secondary.saving_box_box_transaction_repository import ISavingBoxBoxTransactionRepository
from domain.ports.secondary.saving_box_amount_box_transaction_repository import ISavingBoxAmountBoxTransactionRepository
from domain.ports.secondary.transaction_type_repository import ITransactionTypeRepository
from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.ports.primary.role_service import IRoleService
from domain.ports.primary.saving_box_box_transaction_service import ISavingBoxBoxTransactionService
from domain.ports.primary.user_service import IUserService
from domain.ports.primary.box_service import IBoxService
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.secondary.box_repository import IBoxRepository
from domain.ports.secondary.amount_box_repository import IAmountBoxRepository
from domain.ports.secondary.amount_box_box_transaction_repository import IAmountBoxBoxTransactionRepository
from domain.ports.primary.saving_box_amount_box_transaction_service import ISavingBoxAmountBoxTransactionService
from domain.ports.primary.box_clean_up_event_service import IBoxCleanUpEventService
from domain.ports.primary.box_clean_up_detail_service import IBoxCleanUpDetailService
from domain.ports.primary.amount_box_clean_up_service import IAmountBoxCleanUpService
from domain.ports.secondary.box_clean_up_event_repository import IBoxCleanUpEventRepository
from domain.ports.secondary.box_clean_up_detail_repository import IBoxCleanUpDetailRepository
from domain.ports.secondary.amount_box_clean_up_repository import IAmountBoxCleanUpRepository
from domain.ports.secondary.amount_box_transaction_repository import IAmountBoxTransactionRepository
from domain.ports.primary.clean_box_service import ICleanBoxService
from application.services.clean_box_service import CleanBoxService
from domain.ports.primary.transaction_type_service import ITransactionTypeService
from application.services.transaction_type_service import TransactionTypeService
from application.services.amount_box_box_transaction_service import AmountBoxBoxTransactionService
# Luego importamos las implementaciones
from adapters.secondary.user_repository import UserRepository
from adapters.secondary.role_repository import RoleRepository
from adapters.secondary.session_repository import SessionRepository
from adapters.secondary.unit_of_work import UnitOfWork
from adapters.secondary.gmail_email_sender import GmailEmailSender
from adapters.secondary.password_reset_repository import PasswordResetRepository
from adapters.secondary.amount_box_transaction_repository import AmountBoxTransactionRepository
from adapters.secondary.saving_box_box_transaction_repository import SavingBoxBoxTransactionRepository
from adapters.secondary.saving_box_amount_box_transaction_repository import SavingBoxAmountBoxTransactionRepository
from adapters.secondary.saving_box_repository import SavingBoxRepository
from adapters.secondary.box_repository import BoxRepository
from adapters.secondary.amount_box_repository import AmountBoxRepository
from adapters.secondary.amount_box_box_transaction_repositoy import AmountBoxBoxTransactionRepository
from application.services.amount_box_transaction_service import AmountBoxTransactionService
from adapters.secondary.transaction_type_repository import TransactionTypeRepository
from application.services.role_service import RoleService
from application.services.saving_box_box_transaction_service import SavingBoxBoxTransactionService
from application.services.user_service import UserService
from application.services.box_service import BoxService
from application.services.amount_box_service import AmountBoxService
from application.services.box_transaction_service import BoxTransactionService
from application.services.saving_box_amount_box_transaction import SavingBoxAmountBoxTransactionService
from application.services.box_clean_up_event_service import BoxCleanUpEventService
from application.services.box_clean_up_detail_service import BoxCleanUpDetailService
from application.services.amount_box_clean_up_service import AmountBoxCleanUpService
from adapters.secondary.box_clean_up_event_repositoy import BoxCleanUpEventRepository
from adapters.secondary.box_clean_up_detail_repository import BoxCleanUpDetailRepository
from adapters.secondary.amount_clean_up_repository import AmountBoxCleanUpRepository
from adapters.secondary.amount_box_transaction_repository import AmountBoxTransactionRepository
from domain.ports.primary.amount_box_box_transaction_service import IAmountBoxBoxTransactionService
from domain.ports.secondary.box_transaction_repository import IBoxTransactionRepository
from domain.ports.primary.box_transaction_service import IBoxTransactionService
from adapters.secondary.box_transaction_repository import BoxTransactionRepository
# Importamos el Container al final para evitar problemas de dependencias circulares
from infrastructure.configuration.container import Container

print("Registrando IUserRepository en el contenedor")
Container.register(IUserRepository, UserRepository, lifetime=Container.Lifetime.TRANSIENT)
print("Registrando IRoleRepository en el contenedor")
Container.register(IRoleRepository, RoleRepository, lifetime=Container.Lifetime.TRANSIENT)
print("Registrando ISessionRepository en el contenedor")
Container.register(ISessionRepository, SessionRepository, lifetime=Container.Lifetime.TRANSIENT)
print("Registrando IPasswordResetRepository en el contenedor")
Container.register(IPasswordResetRepository, PasswordResetRepository, lifetime=Container.Lifetime.TRANSIENT)
print("Registrando IUnitOfWork en el contenedor")
Container.register(IUnitOfWork, UnitOfWork, lifetime=Container.Lifetime.SCOPED)
print("Registrando IEmailSender en el contenedor")
Container.register(IEmailSender, GmailEmailSender, lifetime=Container.Lifetime.SINGLETON)
print("Registrando IAmountBoxTransactionService en el contenedor")
Container.register(IAmountBoxTransactionService, AmountBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
print("Registrando ISavingBoxRepository en el contenedor")
Container.register(ISavingBoxRepository, SavingBoxRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando ISavingBoxBoxTransactionRepository en el contenedor")
Container.register(ISavingBoxBoxTransactionRepository, SavingBoxBoxTransactionRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando ISavingBoxAmountBoxTransactionRepository en el contenedor")
Container.register(ISavingBoxAmountBoxTransactionRepository, SavingBoxAmountBoxTransactionRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando ITransactionTypeRepository en el contenedor")
Container.register(ITransactionTypeRepository, TransactionTypeRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IBoxRepository en el contenedor")
Container.register(IBoxRepository, BoxRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IAmountBoxRepository en el contenedor")
Container.register(IAmountBoxRepository, AmountBoxRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IAmountBoxBoxTransactionRepository en el contenedor")
Container.register(IAmountBoxBoxTransactionRepository, AmountBoxBoxTransactionRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IBoxCleanUpEventRepository en el contenedor")
Container.register(IBoxCleanUpEventRepository, BoxCleanUpEventRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IBoxCleanUpDetailRepository en el contenedor")
Container.register(IBoxCleanUpDetailRepository, BoxCleanUpDetailRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IAmountBoxCleanUpRepository en el contenedor")
Container.register(IAmountBoxCleanUpRepository, AmountBoxCleanUpRepository, lifetime=Container.Lifetime.SCOPED)
print("Registrando IAmountBoxTransactionRepository en el contenedor")
Container.register(IAmountBoxTransactionRepository, AmountBoxTransactionRepository, lifetime=Container.Lifetime.SCOPED)
Container.register(ITransactionTypeService, TransactionTypeService)
Container.register(IBoxTransactionRepository, BoxTransactionRepository, lifetime=Container.Lifetime.SCOPED)

# Registramos los servicios de forma lazy para evitar importaciones circulares
def register_services():
    """Registra los servicios de aplicación de forma lazy"""
    from application.services.user_registration_service import UserRegistrationService
    from application.services.authentication_service import AuthenticationService
    from application.services.session_service import SessionService
    from application.services.user_login_service import UserLoginService
    from application.services.password_reset_service import PasswordResetService
    from application.services.amount_box_transaction_service import AmountBoxTransactionService
    from application.services.saving_box_service import SavingBoxService
    from application.services.box_service import BoxService
    from application.services.amount_box_service import AmountBoxService
    from application.services.amount_box_transaction_service import AmountBoxTransactionService
    print("Registrando IUserRegistrationService en el contenedor")
    Container.register(IUserRegistrationService, UserRegistrationService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAuthenticationService en el contenedor")
    Container.register(IAuthenticationService, AuthenticationService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ISessionService en el contenedor")
    Container.register(ISessionService, SessionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IUserLoginService en el contenedor")
    Container.register(IUserLoginService, UserLoginService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IPasswordResetService en el contenedor")
    Container.register(IPasswordResetService, PasswordResetService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAmountBoxTransactionService en el contenedor")
    Container.register(IAmountBoxTransactionService, AmountBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ISavingBoxService en el contenedor")
    Container.register(ISavingBoxService, SavingBoxService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ISavingBoxTransactionService en el contenedor")
    Container.register(ISavingBoxBoxTransactionService, SavingBoxBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ISavingBoxAmountBoxTransactionService en el contenedor")
    Container.register(ISavingBoxAmountBoxTransactionService, SavingBoxAmountBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IRoleService en el contenedor")
    Container.register(IRoleService, RoleService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IUserService en el contenedor")
    Container.register(IUserService, UserService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IBoxService en el contenedor")
    Container.register(IBoxService, BoxService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAmountBoxService en el contenedor")
    Container.register(IAmountBoxService, AmountBoxService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IBoxCleanUpEventService en el contenedor")
    Container.register(IBoxCleanUpEventService, BoxCleanUpEventService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IBoxCleanUpDetailService en el contenedor")
    Container.register(IBoxCleanUpDetailService, BoxCleanUpDetailService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAmountBoxCleanUpService en el contenedor")
    Container.register(IAmountBoxCleanUpService, AmountBoxCleanUpService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAmountBoxTransactionService en el contenedor")
    Container.register(IAmountBoxTransactionService, AmountBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ICleanBoxService en el contenedor")
    Container.register(ICleanBoxService, CleanBoxService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando ISavingBoxBoxTransactionService en el contenedor")
    Container.register(ISavingBoxBoxTransactionService, SavingBoxBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IAmountBoxBoxTransactionService en el contenedor")
    Container.register(IAmountBoxBoxTransactionService, AmountBoxBoxTransactionService, lifetime=Container.Lifetime.SCOPED)
    print("Registrando IBoxTransactionService en el contenedor")
    Container.register(IBoxTransactionService, BoxTransactionService, lifetime=Container.Lifetime.SCOPED)
# Llamamos a la función para registrar los servicios
register_services()