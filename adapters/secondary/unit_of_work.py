from django.db import transaction
from domain.ports.secondary.unit_of_work import IUnitOfWork
import logging

logger = logging.getLogger(__name__)

class UnitOfWork(IUnitOfWork):
    """
    Implementación de Unit of Work para PostgreSQL usando Django ORM
    
    Esta clase maneja transacciones de base de datos de forma abstracta,
    permitiendo coordinar múltiples operaciones como una sola unidad atómica.
    """
    
    def __init__(self):
        """
        Inicializa el Unit of Work
        
        _transaction: Contiene la transacción activa de Django
        _is_active: Indica si hay una transacción activa
        """
        self._transaction = None
        self._is_active = False
    
    def begin_transaction(self) -> None:
        """
        Inicia una nueva transacción de base de datos
        
        Esta función:
        1. Crea un contexto de transacción atómica de Django
        2. Entra al contexto (inicia la transacción)
        3. Marca la transacción como activa
        
        Django ORM automáticamente:
        - Inicia un BEGIN TRANSACTION en PostgreSQL
        - Configura el nivel de aislamiento (por defecto READ COMMITTED)
        - Prepara el contexto para operaciones de BD
        """
        if self._is_active:
            logger.warning("Intento de iniciar transacción cuando ya hay una activa")
            return
        
        try:
            # transaction.atomic() es una función de Django que:
            # - Crea un contexto de transacción atómica
            # - Maneja automáticamente el BEGIN/COMMIT/ROLLBACK
            # - Es compatible con PostgreSQL
            self._transaction = transaction.atomic()
            
            # __enter__() inicia la transacción en PostgreSQL
            # Equivale a ejecutar: BEGIN TRANSACTION;
            self._transaction.__enter__()
            
            self._is_active = True
            logger.debug("Transacción iniciada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al iniciar transacción: {str(e)}")
            self._transaction = None
            self._is_active = False
            raise
    
    def commit(self) -> None:
        """
        Confirma los cambios en la base de datos
        
        Esta función:
        1. Verifica que hay una transacción activa
        2. Confirma todos los cambios realizados
        3. Cierra la transacción
        4. Limpia el estado
        
        En PostgreSQL esto equivale a:
        - COMMIT; (confirma todos los cambios)
        - Libera locks de filas/tablas
        - Hace los cambios visibles a otras transacciones
        """
        if not self._is_active or not self._transaction:
            logger.warning("Intento de commit sin transacción activa")
            return
        
        try:
            # __exit__(None, None, None) confirma la transacción
            # Los parámetros None indican:
            # - No hay excepción (None)
            # - No hay tipo de excepción (None) 
            # - No hay traceback (None)
            self._transaction.__exit__(None, None, None)
            
            self._transaction = None
            self._is_active = False
            logger.debug("Transacción confirmada exitosamente")
            
        except Exception as e:
            logger.error(f"Error al confirmar transacción: {str(e)}")
            self._transaction = None
            self._is_active = False
            raise
    
    def rollback(self) -> None:
        """
        Revierte los cambios en la base de datos
        
        Esta función:
        1. Verifica que hay una transacción activa
        2. Revierte todos los cambios realizados
        3. Cierra la transacción
        4. Limpia el estado
        
        En PostgreSQL esto equivale a:
        - ROLLBACK; (revierte todos los cambios)
        - Libera locks de filas/tablas
        - Restaura el estado anterior
        """
        if not self._is_active or not self._transaction:
            logger.warning("Intento de rollback sin transacción activa")
            return
        
        try:
            # __exit__(Exception, None, None) revierte la transacción
            # El primer parámetro Exception fuerza el rollback
            # Los otros parámetros None indican no hay tipo/traceback específico
            self._transaction.__exit__(Exception("Rollback"), None, None)
            
            self._transaction = None
            self._is_active = False
            logger.debug("Transacción revertida exitosamente")
            
        except Exception as e:
            logger.error(f"Error al revertir transacción: {str(e)}")
            self._transaction = None
            self._is_active = False
            raise
    
    @property
    def is_active(self) -> bool:
        """
        Propiedad que indica si hay una transacción activa
        
        Útil para verificar el estado antes de operaciones
        """
        return self._is_active
    
    def __enter__(self):
        """
        Permite usar el Unit of Work como context manager
        
        Ejemplo:
        with UnitOfWork() as uow:
            uow.begin_transaction()
            # ... operaciones ...
            uow.commit()
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """
        Maneja la salida del context manager
        
        Si hay una excepción, hace rollback automático
        Si no hay excepción, hace commit automático
        """
        if self._is_active:
            if exc_type is not None:
                # Hay una excepción, hacer rollback
                self.rollback()
            else:
                # No hay excepción, hacer commit
                self.commit()