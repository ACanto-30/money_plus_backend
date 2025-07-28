from domain.ports.secondary.saving_box_repository import ISavingBoxRepository
from domain.entities.saving_box import SavingBox
from typing import List
from domain.exceptions.implementations import InvalidDomainOperationException
from infrastructure.persistence.models import SavingBox as SavingBoxModel
from infrastructure.persistence.models import User

class SavingBoxRepository(ISavingBoxRepository):
    """Implementacion del repositorio de SavingBox"""

    def get_saving_box_by_user_id(self, user_id: int) -> SavingBox:
        """Metodo para obtener la caja de ahorro por el id del usuario"""
        saving_box = SavingBoxModel.objects.get(user_id=user_id)
        if saving_box is None:
            raise InvalidDomainOperationException("caja de ahorro", user_id, "No se encontró la caja de ahorro")
        return saving_box.to_domain_entity()

    def get_all_saving_boxes_by_user_id(self, user_id: int) -> List[SavingBox]:
        """Metodo para obtener todas las cajas de ahorro por el id del usuario"""
        saving_boxes = SavingBoxModel.objects.filter(user_id=user_id)
        if saving_boxes is None:
            raise InvalidDomainOperationException("caja de ahorro", user_id, "No se encontraron cajas de ahorro")
        return [saving_box.to_domain_entity() for saving_box in saving_boxes]

    def create_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para crear una caja de ahorro"""
        # Obtener la instancia de User
        user_instance = User.objects.get(id=saving_box.user_id)
        
        saving_box_model = SavingBoxModel.objects.create(user=user_instance)
        if saving_box_model is None:
            raise InvalidDomainOperationException("caja de ahorro", saving_box.user_id, "No se pudo crear la caja de ahorro")
        return saving_box_model.to_domain_entity()
    
    def update_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para actualizar una caja de ahorro"""
        saving_box_model = SavingBoxModel.objects.get(id=saving_box.id)
        if saving_box_model is None:
            raise InvalidDomainOperationException("caja de ahorro", saving_box.id, "No se encontró la caja de ahorro")
        saving_box_model.amount = saving_box.amount
        saving_box_model.save()
        return saving_box_model.to_domain_entity()
    
    def delete_saving_box(self, saving_box_id: int) -> bool:
        """Metodo para eliminar una caja de ahorro"""
        saving_box = SavingBoxModel.objects.get(id=saving_box_id)
        if saving_box is None:
            raise InvalidDomainOperationException("caja de ahorro", saving_box_id, "No se encontró la caja de ahorro")
        saving_box.delete()
        return True

    def withdraw_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para retirar dinero de una caja de ahorro (unica por usuario), el dinero ya contado o descontado del service
        solo listo para actualizar el estado de la caja de ahorro"""
        saving_box_model = SavingBoxModel.objects.filter(id=saving_box.id).update(amount=saving_box.amount)
        if saving_box_model == 0:
            raise InvalidDomainOperationException("caja de ahorro", saving_box.id, "No se encontró la caja de ahorro")
        # Ya todo el dinero ya fue contado o descontado del service
        return saving_box.to_domain_entity()
    
    def deposit_saving_box(self, saving_box: SavingBox) -> SavingBox:
        """Metodo para depositar dinero en una caja de ahorro (unica por usuario), el dinero ya contado o descontado del service
        solo listo para actualizar el estado de la caja de ahorro"""
        saving_box_model = SavingBoxModel.objects.filter(id=saving_box.id).update(amount=saving_box.amount)
        if saving_box_model == 0:
            raise InvalidDomainOperationException("caja de ahorro", saving_box.id, "No se encontró la caja de ahorro")
        # Ya todo el dinero ya fue contado o descontado del service
        return saving_box.to_domain_entity()

    def get_saving_box_by_id(self, saving_box_id: int) -> SavingBox:
        """Metodo para obtener la caja de ahorro por el id"""
        print("Llego hasta aqui antes de obtener la caja de ahorro por el id")
        print("saving_box_id:", saving_box_id)
        print("SavingBoxModel.objects:", SavingBoxModel.objects)
        print("SavingBoxModel.objects.get(id=saving_box_id):", SavingBoxModel.objects.get(id=saving_box_id))
        saving_box = SavingBoxModel.objects.get(id=saving_box_id)
        print("saving_box:", saving_box)
        if saving_box is None:
            raise InvalidDomainOperationException("caja de ahorro", saving_box_id, "No se encontró la caja de ahorro")
        print("saving_box.to_domain_entity():", saving_box.to_domain_entity())
        print("Llego hasta aqui despues de obtener la caja de ahorro por el id")
        return saving_box.to_domain_entity()