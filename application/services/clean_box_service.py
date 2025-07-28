from domain.ports.primary.clean_box_service import ICleanBoxService
from infrastructure.configuration.container import Container
from domain.ports.primary.box_service import IBoxService
from domain.ports.primary.amount_box_service import IAmountBoxService
from domain.ports.primary.saving_box_service import ISavingBoxService
from domain.exceptions.implementations import InvalidDomainOperationException
from domain.ports.secondary.unit_of_work import IUnitOfWork
from domain.ports.primary.saving_box_box_transaction_service import ISavingBoxBoxTransactionService
from domain.commands.box_transfer_command import BoxTransferCommand
from domain.entities.transaction_type import TransactionTypeEnum
from domain.entities.box_clean_up_detail import BoxCleanUpDetail
from domain.entities.box_clean_up_event import BoxCleanUpEvent
from domain.ports.primary.box_clean_up_event_service import IBoxCleanUpEventService
from django.utils import timezone
from typing import List
from domain.entities.box import Box
from domain.ports.primary.amount_box_transaction_service import IAmountBoxTransactionService
from domain.commands.box_transaction_command import BoxTransactionCommand
from domain.ports.primary.box_clean_up_detail_service import IBoxCleanUpDetailService
from domain.entities.saving_box_amount_box_transaction import SavingBoxAmountBoxTransaction
from domain.ports.primary.saving_box_amount_box_transaction_service import ISavingBoxAmountBoxTransactionService

class CleanBoxService(ICleanBoxService):
    def __init__(self):
        # Inicializar solo servicios que proporcionan los metodos que se van a usar
        self._box_service = Container.resolve(IBoxService)
        self._amount_box_service = Container.resolve(IAmountBoxService)
        self._unit_of_work = Container.resolve(IUnitOfWork)
        self._saving_box_service = Container.resolve(ISavingBoxService)
        self._saving_box_box_transaction_service = Container.resolve(ISavingBoxBoxTransactionService)
        self._box_clean_up_event_service = Container.resolve(IBoxCleanUpEventService)
        self._amount_box_transaction_service = Container.resolve(IAmountBoxTransactionService)
        self._box_clean_up_detail_service = Container.resolve(IBoxCleanUpDetailService)
        self._saving_box_amount_box_transaction_service = Container.resolve(ISavingBoxAmountBoxTransactionService)
    def clean_box(self, box_id: int) -> int:
        """Limpia una caja"""

        

        box = self._box_service.get_box_by_id(box_id)

        if not box:
            raise InvalidDomainOperationException("caja", box_id, "La caja no existe")

        box_amount = box.amount

        # Prepara box entity para hacer la limpieza (transaccion)

        # Llamar al metodo de limpieza de la caja
        self._box_service.make_box_transaction(box.clean())

        return box_amount

    def clean_amount_box(self, amount_box_id: int) -> int:
        """Limpia una caja de amount"""
        amount_box = self._amount_box_service.get_amount_box_by_id(amount_box_id)

        if not amount_box:
            raise InvalidDomainOperationException("caja de amount", amount_box_id, "La caja de amount no existe")
        
        amount_box_amount = amount_box.amount
        
        # Limpiar caja
        self._amount_box_service.make_amount_box_transaction(amount_box.clean())

        return amount_box_amount

    def clean_all_boxes_by_user_id(self, user_id: int) -> bool:
        """Limpia todas las cajas de un usuario y el monto total de todo transferirlo a la caja de ahorros"""

        try:

            print("Llego hasta aqui empezando la transaccion")
            # EMPEZAR TRANSACCION
            self._unit_of_work.begin_transaction()

            # Definir la fecha de limpieza
            date_box_clean_up = timezone.now()

            # Obtener todas las cajas del usuario
            boxes = self._box_service.get_all_boxes_by_user_id(user_id)

            # Obtener el amount_box del usuario
            amount_box = self._amount_box_service.get_amount_box_by_user_id(user_id)

            if not amount_box:
                raise InvalidDomainOperationException("caja de amount", user_id, "La caja de amount no existe")

            # Obtener la caja de ahorros del usuario
            print("Llego hasta aqui antes de obtener la caja de ahorros")
            print("user_id:", user_id)
            saving_box = self._saving_box_service.get_saving_box_by_user_id(user_id)

            if not saving_box:
                raise InvalidDomainOperationException("caja de ahorros", user_id, "La caja de ahorros no existe")

            print("Llego hasta aqui antes de obtener el total de dinero")

            # Obtener el total de dinero de las cajas que es igual al amount de boxes y de amount_box para registrarlo en una tabla aparte
            
            total_amount = sum(box.amount for box in boxes) + amount_box.amount
            print("total_amount:", total_amount)
            print("amount_box.amount:", amount_box.amount)
            print("sum(box.amount for box in boxes):", sum(box.amount for box in boxes))


            
            # Regitrar en box_clean_up_event
            box_clean_up_event = BoxCleanUpEvent(
                user_id=user_id,
                total_amount=total_amount,
                created_at=date_box_clean_up,
                updated_at=date_box_clean_up
            )

            print("Llego hasta aqui antes de registrar en box_clean_up_event")
            # Registrar en box_clean_up_event
            box_clean_up_event_result = self._box_clean_up_event_service.register_box_clean_up_event(box_clean_up_event)

            print("Llego hasta aqui antes de crear el command para la transaccion")
            # Crear command para la transaccion
            amount_box_command = BoxTransactionCommand(
                box_id=amount_box.id,
                amount=amount_box.amount,
                transaction_type_id=TransactionTypeEnum.CLEAN_BOX.value,
                user_id=user_id,
                created_at=date_box_clean_up,
                updated_at=date_box_clean_up
                )

            # Guarda el valor original antes de limpiar
            amount_box_original_amount = amount_box.amount

            # Registrar la transaccion de amount en saving_box_amount_box_transaction
            saving_box_amount_box_transaction = SavingBoxAmountBoxTransaction(
                saving_box_id=saving_box.id,
                amount_box_id=amount_box.id,
                amount=amount_box_original_amount,
                transaction_type_id=TransactionTypeEnum.CLEAN_BOX.value,
                created_at=date_box_clean_up,
                updated_at=date_box_clean_up
            )

            # Sumar el dinero del amount_box al saving_box
            saving_box.amount += amount_box_original_amount
            saving_box.updated_at = date_box_clean_up
            self._saving_box_service.make_saving_box_transaction(saving_box)

            # Limpiar amount_box
            self._amount_box_transaction_service.make_amount_box_transaction(amount_box_command)
            # Sumar el dinero de amount_box al saving_box
            saving_box.amount += amount_box_original_amount
            # Registrar la transaccion en saving_box_amount_box_transaction
            self._saving_box_amount_box_transaction_service.make_amount_box_saving_box_transaction(saving_box_amount_box_transaction)

            print("Llego hasta aqui antes de verificar si existen cajas para limpiar")

            # Verificar que existan cajas para limpiar, de existir se ejecuta el for, de no existir se ejecuta otra cosa
            if len(boxes) > 0:
                # Limpiar cajas, transferir el dinero a la caja de ahorros, y registrar la transaccion en saving_box_box_transaction
                for box in boxes:
                    # Registrar la transaccion en saving_box_box_transaction
                    print("Llego hasta aqui antes de crear el command para la transaccion")
                    # Crear command para la transaccion
                    print("box.id:", box.id)
                    print("saving_box.id:", saving_box.id)
                    print("user_id:", user_id)
                    command = BoxTransferCommand(
                        from_box_id=box.id,
                        to_box_id=saving_box.id,
                        amount=box.amount,
                        user_id=user_id,
                        transaction_type_id=TransactionTypeEnum.CLEAN_BOX.value,
                        created_at=date_box_clean_up,
                        updated_at=date_box_clean_up
                    )

                    # Registrar la transaccion en saving_box_box_transaction
                    print("Llego hasta aqui antes de hacer la transaccion")
                    self._saving_box_box_transaction_service.make_box_saving_box_transaction(command)

                    # Registrar en el box_clean_up_detail
                    print("Llego hasta aqui antes de crear el box_clean_up_detail")
                    box_clean_up_detail = BoxCleanUpDetail(
                        box_id=box.id,
                        amount=box.amount,
                        box_cleanup_event_id=box_clean_up_event_result.id,
                        created_at=date_box_clean_up,
                        updated_at=date_box_clean_up
                    )

                    print("Llego hasta aqui antes de registrar en el box_clean_up_detail")
                    # Registrar en el box_clean_up_detail
                    self._box_clean_up_detail_service.register_box_clean_up_detail(box_clean_up_detail)
                    print("Llego hasta aqui despues de registrar en el box_clean_up_detail")

            

            # TERMINAR TRANSACCION
            self._unit_of_work.commit()

            # Retorna true si la transaccion se realizo correctamente
            return True
        
        # Si ocurre un error, se hace un rollback de la transaccion
        except Exception as e:
            self._unit_of_work.rollback()
            raise

    def get_all_boxes_by_user_id(self, user_id: int) -> List[Box]:
        return self._box_service.get_all_boxes_by_user_id(user_id)

    def get_all_box_clean_up_events_by_user_id(self, user_id: int) -> List[BoxCleanUpEvent]:
        return self._box_clean_up_event_service.get_all_box_clean_up_events_by_user_id(user_id)