from domain.ports.secondary.box_repository import IBoxRepository
from domain.entities.box import Box
from typing import List
from infrastructure.persistence.models import Box as BoxModel

class BoxRepository(IBoxRepository):

    def save_box(self, user_id: int, name: str) -> Box:
        """Metodo para guardar una caja"""
        box_model = BoxModel(
            user_id=user_id,
            amount=0,
            is_active=True,
            name=name
        )
        box_model.save()
        return box_model.to_domain_entity()

    def get_box_active_by_id(self, box_id: int) -> Box:
        """Metodo para obtener la caja por el id y que este activa"""
        box_model = BoxModel.objects.get(id=box_id, is_active=True)
        return box_model.to_domain_entity()
    
    def get_box_active_by_user_id(self, user_id: int) -> Box:
        """Metodo para obtener la caja por el id del usuario y que este activa"""
        box_model = BoxModel.objects.get(user_id=user_id, is_active=True)
        return box_model.to_domain_entity()
    
    def make_box_active_transaction(self, box: Box) -> Box:
        """Metodo para hacer una transaccion en la caja"""
        box_model = BoxModel.objects.get(id=box.id, is_active=True)
        box_model.amount = box.amount
        box_model.save()
        return box_model.to_domain_entity()

    def get_box_active_by_amount_box_id(self, amount_box_id: int) -> Box:
        """Metodo para obtener la caja por el id de la caja de dinero y que este activa"""
        box_model = BoxModel.objects.get(amount_box_id=amount_box_id, is_active=True)
        return box_model.to_domain_entity()
    
    def get_box_active_by_saving_box_id(self, saving_box_id: int) -> Box:
        """Metodo para obtener la caja por el id de la caja de ahorro y que este activa"""
        box_model = BoxModel.objects.get(saving_box_id=saving_box_id, is_active=True)
        return box_model.to_domain_entity()
    
    def get_all_boxes_active_by_user_id(self, user_id: int) -> List[Box]:
        """Metodo para obtener todas las cajas activas por el id del usuario"""
        box_models = BoxModel.objects.filter(user_id=user_id, is_active=True)
        return [box_model.to_domain_entity() for box_model in box_models]

    def make_box_deactive_box(self, box_id: int, user_id: int) -> Box:
        """Metodo para desactivar una caja"""
        box_model = BoxModel.objects.get(id=box_id, user_id=user_id, is_active=True)
        box_model.is_active = False
        box_model.save()
        return box_model.to_domain_entity()

    def is_owner_box(self, box_id: int, user_id: int) -> bool:
        """Metodo para verificar si el usuario es el propietario de la caja"""
        box_model = BoxModel.objects.filter(id=box_id, user_id=user_id, is_active=True)
        return box_model.exists()

    def update_box_name(self, box_id: int, name: str) -> Box:
        """Metodo para actualizar el nombre de la caja"""
        box_model = BoxModel.objects.get(id=box_id, is_active=True)
        box_model.name = name
        box_model.save()
        return box_model.to_domain_entity()