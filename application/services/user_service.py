from domain.ports.primary.user_service import IUserService
from domain.ports.secondary.user_repository import IUserRepository
from infrastructure.configuration.container import Container

from domain.entities.user import User
from domain.exceptions.implementations import InvalidDomainOperationException

class UserService(IUserService):
    def __init__(self):
        self._user_repository = Container.resolve(IUserRepository)

    def get_user_by_id(self, user_id: int) -> User:
        user = self._user_repository.get_by_id(user_id)
        if not user:
            raise InvalidDomainOperationException("User", user_id, "El usuario no existe")
        return user

    def get_user_by_email(self, email: str) -> User:
        user = self._user_repository.get_by_email(email)
        if not user:
            raise InvalidDomainOperationException("User", email, "El usuario no existe")
        return user

    def update_password(self, user_id: int, new_password: str) -> bool:
        return self._user_repository.update_password(user_id, new_password)