from domain.ports.secondary.amount_box_repository import IAmountBoxRepository
from domain.entities.amount_box import AmountBox
from infrastructure.persistence.models import AmountBox as AmountBoxModel
from typing import List
from datetime import datetime

class AmountBoxRepository(IAmountBoxRepository):
    def get_amount_box_by_user_id(self, user_id: int) -> AmountBox:
        """Metodo para obtener la cantidad de la caja por el id del usuario"""
        amount_box_model = AmountBoxModel.objects.get(user_id=user_id)
        return amount_box_model.to_domain_entity()
    
    def get_all_amount_boxes_by_user_id(self, user_id: int) -> List[AmountBox]:
        """Metodo para obtener todas las cantidades de la caja por el id del usuario"""
        amount_box_models = AmountBoxModel.objects.filter(user_id=user_id)
        return [amount_box_model.to_domain_entity() for amount_box_model in amount_box_models]
    
    def create_amount_box(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para crear una nueva caja de dinero"""
        amount_box_model = AmountBoxModel.objects.create(
            user_id=amount_box.user_id,
            amount=amount_box.amount,
            name="caja de dinero"
        )
        print("amount_box_model:", amount_box_model)
        amount_box_model.save()
        print("amount_box_model despues de guardar:", amount_box_model)
        return amount_box_model.to_domain_entity()
    
    def deposit_amount_box(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para depositar una cantidad en la caja"""
        amount_box_model = AmountBoxModel.objects.get(id=amount_box.id)
        amount_box_model.amount += amount_box.amount
        amount_box_model.save()
        return amount_box_model.to_domain_entity()
    
    def make_amount_box_transaction(self, amount_box: AmountBox) -> AmountBox:
        """Metodo para hacer una transaccion en la caja"""
        amount_box_model = AmountBoxModel.objects.get(id=amount_box.id)
        amount_box_model.amount = amount_box.amount
        amount_box_model.save()
        return amount_box_model.to_domain_entity()

    def get_amount_box_by_id(self, amount_box_id: int) -> AmountBox:
        """Metodo para obtener la cantidad de la caja por el id"""
        amount_box_model = AmountBoxModel.objects.get(id=amount_box_id)
        print("amount_box_model:", amount_box_model, type(amount_box_model))
        return amount_box_model.to_domain_entity()

    

        