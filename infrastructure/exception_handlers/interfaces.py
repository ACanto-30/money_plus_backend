from abc import ABC, abstractmethod

class ICustomExceptionHandler(ABC):
    @abstractmethod
    def can_handle(self, exception: Exception) -> bool:
        pass

    @abstractmethod
    def handle(self, request, exception: Exception):
        pass

class IErrorResponseSerializer(ABC):
    @abstractmethod
    def serialize_and_send(self, request, errors: dict, title: str, status_code: int, instance: str):
        pass