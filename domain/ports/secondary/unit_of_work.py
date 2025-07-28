from abc import ABC, abstractmethod

class IUnitOfWork(ABC):
    """Interfaz para Unit of Work"""
    
    @abstractmethod
    def begin_transaction(self) -> None:
        """Inicia una transacción"""
        pass
    
    @abstractmethod
    def commit(self) -> None:
        """Confirma los cambios en la base de datos"""
        pass
    
    @abstractmethod
    def rollback(self) -> None:
        """Revierte los cambios en la base de datos"""
        pass 