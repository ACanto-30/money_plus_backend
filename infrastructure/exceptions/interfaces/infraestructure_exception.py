from abc import ABC, abstractmethod

class IInfraestructureException(ABC):
    @property
    @abstractmethod
    def property_name(self) -> str:
        pass

    @property
    @abstractmethod
    def invalid_value(self):
        pass

    @property
    @abstractmethod
    def message(self) -> str:
        pass