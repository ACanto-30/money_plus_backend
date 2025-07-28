from domain.ports.primary.saving_box_box_transaction_service import ISavingBoxBoxTransactionService
from domain.commands.box_transfer_command import BoxTransferCommand
from domain.ports.primary.box_service import IBoxService
from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.ports.primary.transaction_type_service import ITransactionTypeService
from domain.ports.secondary.unit_of_work import IUnitOfWork
from infrastructure.configuration.container import Container
from domain.entities.transaction_type import TransactionTypeEnum
from domain.exceptions.implementations import InvalidDomainOperationException, ForbiddenDomainOperationException
from domain.ports.secondary.saving_box_box_transaction_repository import ISavingBoxBoxTransactionRepository
from domain.entities.saving_box_box_transaction import SavingBoxBoxTransaction
from django.utils import timezone

class SavingBoxBoxTransactionService(ISavingBoxBoxTransactionService):
    def __init__(self):
        self._saving_box_box_transaction_repository = Container.resolve(ISavingBoxBoxTransactionRepository)
        self._saving_box_service = Container.resolve(ISavingBoxService)
        self._box_service = Container.resolve(IBoxService)
        self._transaction_type_service = Container.resolve(ITransactionTypeService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        
    def make_saving_box_box_transaction(self, command: BoxTransferCommand) -> bool:
        """Metodo para hacer una transaccion de la caja de ahorro a otra box"""
        
        try:

            # EMPEZAR UNA TRANSACCION
            self._unit_of_work.begin_transaction()

            # Definir la fecha de la transaccion
            created_at = command.created_at
            updated_at = command.updated_at

            # Obtener la caja de ahorro origen
            saving_box = self._saving_box_service.get_saving_box_by_id(command.from_box_id)

            # Obtener la caja de destino
            box = self._box_service.get_box_by_id(command.to_box_id)

            # Verificar que el user_id sea el mismo para las dos cajas
            print("saving_box.user_id:", saving_box.user_id)
            print("box.user_id:", box.user_id)
            print("command.user_id:", command.user_id)
            print(saving_box)
            # Verificar que el user_id sea el mismo para las dos cajas
            if saving_box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja de ahorro", command.from_box_id, "La caja de ahorro no pertenece al usuario")
        
            if box.user_id != command.user_id:
                raise ForbiddenDomainOperationException("caja", command.to_box_id, "La caja no pertenece al usuario")

            # Obtener el tipo de transaccion
            transaction_type = self._transaction_type_service.get_transaction_type_by_id(command.transaction_type_id)
        
            # Solamente se puede retirar de la caja de ahorro
            print("Saving box amount:", saving_box.amount)
            if transaction_type.name == TransactionTypeEnum.WITHDRAW.name:
                # Retiro
                saving_box.withdraw_amount(command.amount)
                #Cualquier otro tipo de transaccion no es valido
            else:
                raise InvalidDomainOperationException("tipo de transaccion", command.transaction_type_id, "El tipo de transaccion no es valido")

            # Suma el dinero restado a la caja de ahorro a la caja de destino
            box.amount += command.amount

            # Definimos la fecha de actualizacion en updated_at
            saving_box.updated_at = updated_at
            print("Saving box amount after transaction:", saving_box.amount)
            self._saving_box_service.make_saving_box_transaction(saving_box)

            # Actualizamos el amount de la caja de destino existente
            box.updated_at = updated_at
            self._box_service.make_box_transaction(box)

            # Creamos el detalle de la transaccion
            saving_box_box_transaction = SavingBoxBoxTransaction(
                saving_box_id=command.from_box_id,
                box_id=command.to_box_id,
                amount=command.amount,
                transaction_type_id=transaction_type.id,
                created_at=created_at,
                updated_at=updated_at
            )

            # Agregamos el detalle de la transaccion en la base de datos en la tabla saving_box_box_transaction
            self._saving_box_box_transaction_repository.save(saving_box_box_transaction)

            # Commit de la transaccion
            self._unit_of_work.commit()

            return True
        
        # Si ocurre un error, se hace un rollback de la transaccion
        except Exception as e:
            self._unit_of_work.rollback()
            raise

    def make_box_saving_box_transaction(self, command: BoxTransferCommand) -> bool:
        """Metodo para hacer una transaccion de la caja a la caja de ahorro"""

        # Definir la fecha de la transaccion
        created_at = command.created_at
        updated_at = command.updated_at

        # Obtener la caja de origen
        print("Llego hasta aqui antes de obtener la caja de origen")
        print("command.from_box_id:", command.from_box_id)
        box = self._box_service.get_box_by_id(command.from_box_id)

        # Obtener la caja de ahorro destino
        print("Llego hasta aqui antes de obtener la caja de ahorro destino")
        print("command.to_box_id:", command.to_box_id)
        saving_box = self._saving_box_service.get_saving_box_by_id(command.to_box_id)

        # Verificar que el user_id sea el mismo para las dos cajas
        if box.user_id != command.user_id:
            raise ForbiddenDomainOperationException("caja", command.from_box_id, "La caja no pertenece al usuario")
    
        if saving_box.user_id != command.user_id:
            raise ForbiddenDomainOperationException("caja de ahorro", command.to_box_id, "La caja de ahorro no pertenece al usuario")

        # Obtener el tipo de transaccion
        print("Llego hasta aqui antes de obtener el tipo de transaccion")
        print("command.transaction_type_id:", command.transaction_type_id)
        transaction_type = self._transaction_type_service.get_transaction_type_by_id(command.transaction_type_id)
        print("transaction_type:", transaction_type)
        print("Llego hasta aqui despues de obtener el tipo de transaccion")
    
        # Solamente se puede depositar en la caja de ahorro
        if transaction_type.name == TransactionTypeEnum.CLEAN_BOX.name:
            # Quitamos el dinero de amount box para depositarlo en la caja de ahorro
            print("Llego hasta aqui antes de limpiar la caja")
            box.clean()
            #Cualquier otro tipo de transaccion no es valido
        else:
            raise InvalidDomainOperationException("tipo de transaccion", command.transaction_type_id, "El tipo de transaccion no es valido")
        print("Llego hasta aqui despues de limpiar la caja")
        # Sumamos el dinero restado de amount box a la caja de ahorro
        saving_box.amount += command.amount

        # Definimos la fecha de actualizacion en updated_at
        box.updated_at = updated_at
        print("Llego hasta aqui antes de actualizar el amount de la caja")
        # Actualizamos el amount de la caja existente
        self._box_service.make_box_transaction(box)
        print("Llego hasta aqui despues de actualizar el amount de la caja")

        # Ahora registramos los detalles de la transaccion en la base de datos en la tabla saving_box_box_transaction
        saving_box_box_transaction = SavingBoxBoxTransaction(
            saving_box_id=command.to_box_id,
            box_id=command.from_box_id,
            amount=command.amount,
            transaction_type_id=transaction_type.id,
            created_at=created_at,
            updated_at=updated_at
        )
        print("saving_box_box_transaction:", saving_box_box_transaction)
        print("saving_box.saving_box_id:", saving_box.id)
        # Definimos la fecha de actualizacion en updated_at
        saving_box.updated_at = updated_at
        print("Llego hasta aqui antes de actualizar el amount de la caja de ahorro")
        # Actualizamos el amount de la caja de ahorro existente
        self._saving_box_service.make_saving_box_transaction(saving_box)
        print("Llego hasta aqui despues de actualizar el amount de la caja de ahorro")
        # Agregamos el detalle de la transaccion en la base de datos en la tabla saving_box_box_transaction
        print("Llego hasta aqui antes de guardar el detalle de la transaccion")
        self._saving_box_box_transaction_repository.save(saving_box_box_transaction)
        print("Llego hasta aqui despues de guardar el detalle de la transaccion")

        return True
        