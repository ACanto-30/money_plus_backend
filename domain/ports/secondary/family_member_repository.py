from abc import ABC, abstractmethod
from domain.entities.family_member import FamilyMember
from domain.entities.family_role import FamilyRole
from typing import List

class IFamilyMemberRepository(ABC):

    @abstractmethod
    def get_all_family_members(self) -> List[FamilyMember]:
        """Metodo para obtener todos los miembros de la familia"""
        pass

    @abstractmethod
    def ban_family_member(self, family_member_id: int) -> bool:
        """Metodo para banear un miembro de la familia"""
        pass

    @abstractmethod
    def unban_family_member(self, family_member_id: int) -> bool:
        """Metodo para desbanear un miembro de la familia"""
        pass
    
    @abstractmethod
    def remove_family_member(self, family_member_id: int) -> bool:
        """Metodo para sacar un miembro de la familia"""
        pass
    
    @abstractmethod
    def get_family_member_role(self, family_member_id: int) -> FamilyRole:
        """Metodo para obtener el rol de un miembro de la familia"""
        pass
    
    @abstractmethod
    def get_family_member_by_user_id(self, user_id: int) -> FamilyMember:
        """Metodo para obtener un miembro de la familia por el id del usuario"""
        pass
    