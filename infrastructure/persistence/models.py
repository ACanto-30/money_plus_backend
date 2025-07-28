from django.db import models
from django.core.validators import EmailValidator
from domain.entities.user import User as UserEntity
from domain.entities.role import Role as RoleEntity
from domain.entities.box import Box as BoxEntity
from domain.entities.family import Family as FamilyEntity
from domain.entities.family_member import FamilyMember as FamilyMemberEntity
from domain.entities.family_role import FamilyRole as FamilyRoleEntity
from domain.entities.loan import Loan as LoanEntity
from domain.entities.loan_state import LoanState as LoanStateEntity
from domain.entities.loan_repayment import LoanRepayment as LoanRepaymentEntity
from domain.entities.session import Session as SessionEntity
from domain.entities.password_reset import PasswordReset as PasswordResetEntity
from domain.value_objects.email import Email
from domain.entities.amount_box_transaction import AmountBoxTransaction as AmountBoxTransactionEntity
from domain.entities.amount_box import AmountBox as AmountBoxEntity
from domain.entities.amount_box_clean_up import AmountBoxCleanUp as AmountBoxCleanUpEntity
from domain.entities.box_clean_up_event import BoxCleanUpEvent as BoxCleanUpEventEntity
from domain.entities.box_clean_up_detail import BoxCleanUpDetail as BoxCleanUpDetailEntity
from domain.entities.transaction_type import TransactionType as TransactionTypeEntity
from domain.entities.amount_box_box_transaction import AmountBoxBoxTransaction as AmountBoxBoxTransactionEntity
from domain.entities.saving_box import SavingBox as SavingBoxEntity
from domain.entities.saving_box_amount_box_transaction import SavingBoxAmountBoxTransaction as SavingBoxAmountBoxTransactionEntity
from domain.entities.saving_box_box_transaction import SavingBoxBoxTransaction as SavingBoxBoxTransactionEntity
from domain.entities.clean_up_schedule import CleanUpSchedule as CleanUpScheduleEntity
from domain.entities.loan_repayment_state import LoanRepaymentState as LoanRepaymentStateEntity
from domain.entities.box_transaction import BoxTransaction as BoxTransactionEntity

class Role(models.Model):
    """Modelo Django para Role"""
    
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'roles'
        verbose_name = 'Role'
        verbose_name_plural = 'Roles'
    
    def __str__(self):
        return f"{self.name} - {self.description}"
    
    def to_domain_entity(self) -> RoleEntity:
        """Convierte a entidad de dominio"""
        return RoleEntity(
            id=self.id,
            name=self.name,
            description=self.description
        )
    
    @classmethod
    def from_domain_entity(cls, role_entity: RoleEntity) -> 'Role':
        """Crea desde entidad de dominio"""
        return cls(
            id=role_entity.id,
            name=role_entity.name,
            description=role_entity.description
        )

class User(models.Model):
    """Modelo Django para User"""
    
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=255)
    email = models.EmailField(unique=True, validators=[EmailValidator()])
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name='users')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['username']),
            models.Index(fields=['email']),
            models.Index(fields=['role']),
        ]
    
    def __str__(self):
        return f"{self.username} - {self.email}"
    
    def to_domain_entity(self) -> UserEntity:
        """Convierte a entidad de dominio"""
        email_vo = Email(self.email)
        return UserEntity(
            id=self.id,
            username=self.username,
            password=self.password,
            email=email_vo,
            role_id=self.role.id
        )
    
    def to_domain_entity_with_boxes(self) -> UserEntity:
        """Convierte a entidad de dominio incluyendo las cajas relacionadas"""
        from .models import Box
        
        email_vo = Email(self.email)
        boxes = []
        
        # Obtener las cajas relacionadas a través de AmountBox
        amount_boxes = self.amount_boxes.all()
        for amount_box in amount_boxes:
            box_entities = [box.to_domain_entity() for box in amount_box.boxes.all()]
            boxes.extend(box_entities)
        
        return UserEntity(
            id=self.id,
            username=self.username,
            password=self.password,
            email=email_vo,
            role_id=self.role.id,
            boxes=boxes
        )
    
    @classmethod
    def from_domain_entity(cls, user_entity: UserEntity) -> 'User':
        """Crea desde entidad de dominio"""
        return cls(
            id=user_entity.id,
            username=user_entity.username,
            password=user_entity.password,
            email=user_entity.email.value if hasattr(user_entity.email, 'value') else user_entity.email,
            role_id=user_entity.role_id
        )

class Box(models.Model):
    """Modelo Django para Box"""
    
    name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    amount = models.IntegerField(default=0)  # en centavos
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='boxes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'boxes'
        verbose_name = 'Box'
        verbose_name_plural = 'Boxes'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['is_active']),
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.name} - ${self.amount}"
    
    def to_domain_entity(self) -> BoxEntity:
        """Convierte a entidad de dominio"""
        return BoxEntity(
            id=self.id,
            name=self.name,
            is_active=self.is_active,
            amount=self.amount,
            user_id=self.user.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, box_entity: BoxEntity) -> 'Box':
        """Crea desde entidad de dominio"""
        return cls(
            id=box_entity.id,
            name=box_entity.name,
            is_active=box_entity.is_active,
            amount=box_entity.amount,
            user_id=box_entity.user_id,
            created_at=box_entity.created_at,
            updated_at=box_entity.updated_at
        )

class Family(models.Model):
    """Modelo Django para Family"""
    
    name = models.CharField(max_length=255)
    family_code = models.CharField(max_length=50, unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'families'
        verbose_name = 'Family'
        verbose_name_plural = 'Families'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['family_code']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.name} - {self.family_code}"
    
    def to_domain_entity(self) -> FamilyEntity:
        """Convierte a entidad de dominio"""
        return FamilyEntity(
            id=self.id,
            name=self.name,
            family_code=self.family_code,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, family_entity: FamilyEntity) -> 'Family':
        """Crea desde entidad de dominio"""
        return cls(
            id=family_entity.id,
            name=family_entity.name,
            family_code=family_entity.family_code,
            is_active=family_entity.is_active,
            created_at=family_entity.created_at,
            updated_at=family_entity.updated_at
        )

class FamilyRole(models.Model):
    """Modelo Django para FamilyRole"""
    
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'family_roles'
        verbose_name = 'Family Role'
        verbose_name_plural = 'Family Roles'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name}"
    
    def to_domain_entity(self) -> FamilyRoleEntity:
        """Convierte a entidad de dominio"""
        return FamilyRoleEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, family_role_entity: FamilyRoleEntity) -> 'FamilyRole':
        """Crea desde entidad de dominio"""
        return cls(
            id=family_role_entity.id,
            name=family_role_entity.name,
            created_at=family_role_entity.created_at,
            updated_at=family_role_entity.updated_at
        )

class FamilyMember(models.Model):
    """Modelo Django para FamilyMember"""
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='members')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='family_memberships')
    is_active = models.BooleanField(default=True)
    is_banned = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'family_members'
        verbose_name = 'Family Member'
        verbose_name_plural = 'Family Members'
        unique_together = ['family', 'user']
        indexes = [
            models.Index(fields=['family']),
            models.Index(fields=['user']),
            models.Index(fields=['is_active']),
            models.Index(fields=['is_banned']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.family.name}"
    
    def to_domain_entity(self) -> FamilyMemberEntity:
        """Convierte a entidad de dominio"""
        return FamilyMemberEntity(
            id=self.id,
            family_id=self.family.id,
            user_id=self.user.id,
            is_active=self.is_active,
            is_banned=self.is_banned,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, family_member_entity: FamilyMemberEntity) -> 'FamilyMember':
        """Crea desde entidad de dominio"""
        return cls(
            id=family_member_entity.id,
            family_id=family_member_entity.family_id,
            user_id=family_member_entity.user_id,
            is_active=family_member_entity.is_active,
            is_banned=family_member_entity.is_banned,
            created_at=family_member_entity.created_at,
            updated_at=family_member_entity.updated_at
        )

class LoanState(models.Model):
    """Modelo Django para LoanState"""
    
    state = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_states'
        verbose_name = 'Loan State'
        verbose_name_plural = 'Loan States'
        indexes = [
            models.Index(fields=['state']),
        ]
    
    def __str__(self):
        return f"{self.state}"
    
    def to_domain_entity(self) -> LoanStateEntity:
        """Convierte a entidad de dominio"""
        return LoanStateEntity(
            id=self.id,
            state=self.state,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, loan_state_entity: LoanStateEntity) -> 'LoanState':
        """Crea desde entidad de dominio"""
        return cls(
            id=loan_state_entity.id,
            state=loan_state_entity.state,
            created_at=loan_state_entity.created_at,
            updated_at=loan_state_entity.updated_at
        )

class Loan(models.Model):
    """Modelo Django para Loan"""
    
    family = models.ForeignKey(Family, on_delete=models.CASCADE, related_name='loans')
    from_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_given')
    to_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loans_received')
    amount = models.IntegerField()
    title = models.CharField(max_length=255)
    state = models.ForeignKey(LoanState, on_delete=models.CASCADE, related_name='loans')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loans'
        verbose_name = 'Loan'
        verbose_name_plural = 'Loans'
        indexes = [
            models.Index(fields=['family']),
            models.Index(fields=['from_user']),
            models.Index(fields=['to_user']),
            models.Index(fields=['state']),
            models.Index(fields=['created_at']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.amount} ({self.state.state})"
    
    def to_domain_entity(self) -> LoanEntity:
        """Convierte a entidad de dominio"""
        return LoanEntity(
            id=self.id,
            family_id=self.family.id,
            from_user_id=self.from_user.id,
            to_user_id=self.to_user.id,
            amount=float(self.amount),
            title=self.title,
            state_id=self.state.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, loan_entity: LoanEntity) -> 'Loan':
        """Crea desde entidad de dominio"""
        return cls(
            id=loan_entity.id,
            family_id=loan_entity.family_id,
            from_user_id=loan_entity.from_user_id,
            to_user_id=loan_entity.to_user_id,
            amount=loan_entity.amount,
            title=loan_entity.title,
            state_id=loan_entity.state_id,
            created_at=loan_entity.created_at,
            updated_at=loan_entity.updated_at
        )

class LoanRepaymentState(models.Model):
    """Modelo Django para LoanRepaymentState"""
    
    state = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_repayment_states'
        verbose_name = 'Loan Repayment State'
        verbose_name_plural = 'Loan Repayment States'
        indexes = [
            models.Index(fields=['state']),
        ]

    def __str__(self):
        return f"{self.state}"
    
    def to_domain_entity(self) -> LoanRepaymentStateEntity:
        """Convierte a entidad de dominio"""
        return LoanRepaymentStateEntity(
            id=self.id,
            state=self.state,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, loan_repayment_state_entity: LoanRepaymentStateEntity) -> 'LoanRepaymentState':
        """Crea desde entidad de dominio"""
        return cls(
            id=loan_repayment_state_entity.id,
            state=loan_repayment_state_entity.state,
            created_at=loan_repayment_state_entity.created_at,
            updated_at=loan_repayment_state_entity.updated_at
        )

class LoanRepayment(models.Model):
    """Modelo Django para LoanRepayment"""
    
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name='repayments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='loan_repayments')
    amount = models.IntegerField()
    title = models.CharField(max_length=255)
    description = models.TextField()
    loan_repayment_state = models.ForeignKey(LoanRepaymentState, on_delete=models.CASCADE, related_name='repayments')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'loan_repayments'
        verbose_name = 'Loan Repayment'
        verbose_name_plural = 'Loan Repayments'
        indexes = [
            models.Index(fields=['loan']),
            models.Index(fields=['user']),
            models.Index(fields=['loan_repayment_state']),
        ]
    
    def __str__(self):
        return f"{self.title} - ${self.amount}"
    
    def to_domain_entity(self) -> LoanRepaymentEntity:
        """Convierte a entidad de dominio"""
        return LoanRepaymentEntity(
            id=self.id,
            loan_id=self.loan.id,
            user_id=self.user.id,
            amount=float(self.amount),
            title=self.title,
            description=self.description,
            loan_repayment_state_id=self.loan_repayment_state.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, loan_repayment_entity: LoanRepaymentEntity) -> 'LoanRepayment':
        """Crea desde entidad de dominio"""
        return cls(
            id=loan_repayment_entity.id,
            loan_id=loan_repayment_entity.loan_id,
            user_id=loan_repayment_entity.user_id,
            amount=loan_repayment_entity.amount,
            title=loan_repayment_entity.title,
            description=loan_repayment_entity.description,
            loan_repayment_state_id=loan_repayment_entity.loan_repayment_state_id,
            created_at=loan_repayment_entity.created_at,
            updated_at=loan_repayment_entity.updated_at
        )

class Session(models.Model):
    """Modelo Django para Session"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sessions')
    refresh_token = models.TextField()
    client_uuid = models.CharField(max_length=255)
    token_created_at = models.DateTimeField()
    expires_at = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'sessions'
        verbose_name = 'Session'
        verbose_name_plural = 'Sessions'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['refresh_token']),
            models.Index(fields=['client_uuid']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_active']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.client_uuid}"
    
    def to_domain_entity(self) -> SessionEntity:
        """Convierte a entidad de dominio"""
        return SessionEntity(
            id=self.id,
            user_id=self.user.id,
            refresh_token=self.refresh_token,
            client_uuid=self.client_uuid,
            token_created_at=self.token_created_at,
            expires_at=self.expires_at,
            is_active=self.is_active,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, session_entity: SessionEntity) -> 'Session':
        """Crea desde entidad de dominio"""
        return cls(
            id=session_entity.id,
            user_id=session_entity.user_id,
            refresh_token=session_entity.refresh_token,
            client_uuid=session_entity.client_uuid,
            token_created_at=session_entity.token_created_at,
            expires_at=session_entity.expires_at,
            is_active=session_entity.is_active,
            created_at=session_entity.created_at,
            updated_at=session_entity.updated_at
        )

class PasswordReset(models.Model):
    """Modelo Django para PasswordReset"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='password_resets')
    code = models.IntegerField(default=0)
    expires_at = models.DateTimeField()
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    is_used = models.BooleanField(default=False)
    class Meta:
        db_table = 'password_resets'
        verbose_name = 'Password Reset'
        verbose_name_plural = 'Password Resets'
        indexes = [
            models.Index(fields=['user']),
            models.Index(fields=['code']),
            models.Index(fields=['expires_at']),
            models.Index(fields=['is_used']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - {self.code}"

    def to_domain_entity(self) -> PasswordResetEntity:
        """Convierte a entidad de dominio"""
        return PasswordResetEntity(
            id=self.id,
            user_id=self.user.id,
            code=self.code,
            expires_at=self.expires_at,
            is_used=self.is_used,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, password_reset_entity: PasswordResetEntity) -> 'PasswordReset':
        """Crea desde entidad de dominio"""
        return cls(
            id=password_reset_entity.id,
            user_id=password_reset_entity.user_id,
            code=password_reset_entity.code,
            expires_at=password_reset_entity.expires_at,
            is_used=password_reset_entity.is_used,
            created_at=password_reset_entity.created_at,
            updated_at=password_reset_entity.updated_at
        )

class AmountBoxBoxTransaction(models.Model):
    """Modelo Django para AmountBoxBoxTransaction"""
    
    amount_box = models.ForeignKey('AmountBox', on_delete=models.CASCADE, related_name='amount_box_box_transactions')
    amount = models.IntegerField()  # en centavos
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, related_name='amount_box_box_transactions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'amount_box_box_transactions'
        verbose_name = 'Amount Box Box Transaction'
        verbose_name_plural = 'Amount Box Box Transactions'
        indexes = [
            models.Index(fields=['amount_box']),
            models.Index(fields=['transaction_type']),
        ]
    
    def __str__(self):
        return f"{self.amount_box.name} - ${self.amount} ({self.transaction_type.name})"
    
    def to_domain_entity(self) -> AmountBoxBoxTransactionEntity:
        """Convierte a entidad de dominio"""
        return AmountBoxBoxTransactionEntity(
            id=self.id,
            amount_box_id=self.amount_box.id,
            amount=float(self.amount),
            transaction_type_id=self.transaction_type.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, box_transaction_entity: AmountBoxBoxTransactionEntity) -> 'AmountBoxBoxTransaction':
        """Crea desde entidad de dominio"""
        return cls(
            id=box_transaction_entity.id,
            amount_box_id=box_transaction_entity.amount_box_id,
            amount=box_transaction_entity.amount,
            transaction_type_id=box_transaction_entity.transaction_type_id,
            created_at=box_transaction_entity.created_at,
            updated_at=box_transaction_entity.updated_at
        )

class AmountBox(models.Model):
    """Modelo Django para AmountBox"""
    
    name = models.CharField(max_length=255)
    amount = models.IntegerField(default=0)  # en centavos
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='amount_boxes')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'amount_boxes'
        verbose_name = 'Amount Box'
        verbose_name_plural = 'Amount Boxes'
        indexes = [
            models.Index(fields=['name']),
            models.Index(fields=['user_id']),
        ]
    
    def __str__(self):
        return f"{self.name} - ${self.amount}"
    
    def to_domain_entity(self) -> AmountBoxEntity:
        """Convierte a entidad de dominio"""
        return AmountBoxEntity(
            id=self.id,
            name=self.name,
            amount=self.amount,
            user_id=self.user.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, amount_box_entity: AmountBoxEntity) -> 'AmountBox':
        """Crea desde entidad de dominio"""
        return cls(
            id=amount_box_entity.id,
            name=amount_box_entity.name,
            amount=amount_box_entity.amount,
            user_id=amount_box_entity.user_id,
            created_at=amount_box_entity.created_at,
            updated_at=amount_box_entity.updated_at
        )

class AmountBoxTransaction(models.Model):
    amount_box = models.ForeignKey('AmountBox', on_delete=models.CASCADE, related_name='amount_box_transactions')
    amount = models.IntegerField()  # en centavos
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, related_name='amount_box_transactions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amount_box_transactions'
        verbose_name = 'Amount Box Transaction'
        verbose_name_plural = 'Amount Box Transactions'
        indexes = [
            models.Index(fields=['amount_box']),
            models.Index(fields=['transaction_type']),
        ]
    
    def __str__(self):
        return f"{self.amount_box.name} - ${self.amount} ({self.transaction_type.name})"
    
    def to_domain_entity(self) -> AmountBoxTransactionEntity:
        """Convierte a entidad de dominio"""
        return AmountBoxTransactionEntity(
            id=self.id,
            amount_box_id=self.amount_box.id,
            amount=float(self.amount),
            transaction_type_id=self.transaction_type.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, amount_box_transaction_entity: AmountBoxTransactionEntity) -> 'AmountBoxTransaction':
        """Crea desde entidad de dominio"""
        return cls(
            id=amount_box_transaction_entity.id,
            amount_box_id=amount_box_transaction_entity.amount_box_id,
            amount=amount_box_transaction_entity.amount,
            transaction_type_id=amount_box_transaction_entity.transaction_type_id,
            created_at=amount_box_transaction_entity.created_at,
            updated_at=amount_box_transaction_entity.updated_at
        )

class SavingBox(models.Model):
    """Modelo Django para SavingBox"""
    
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='saving_boxes')
    amount = models.IntegerField(default=0)  # en centavos
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'saving_boxes'
        verbose_name = 'Saving Box'
        verbose_name_plural = 'Saving Boxes'
        indexes = [
            models.Index(fields=['user']),
        ]
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount}"
    
    def to_domain_entity(self) -> SavingBoxEntity:
        """Convierte a entidad de dominio"""
        return SavingBoxEntity(
            id=self.id,
            user_id=self.user.id,
            amount=float(self.amount),
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, saving_box_entity: SavingBoxEntity) -> 'SavingBox':
        """Crea desde entidad de dominio"""
        return cls(
            id=saving_box_entity.id,
            user_id=saving_box_entity.user_id,  # Asegura que se use user_id, no user
            amount=saving_box_entity.amount,
            created_at=saving_box_entity.created_at,
            updated_at=saving_box_entity.updated_at
        )

class AmountBoxCleanUp(models.Model):
    """Modelo Django para AmountBoxCleanUp"""
    amount_box_id = models.ForeignKey('AmountBox', on_delete=models.CASCADE, related_name='cleanups')
    total_amount = models.IntegerField()  # en centavos
    box_cleanup_event_id = models.ForeignKey('BoxCleanUpEvent', on_delete=models.CASCADE, related_name='amount_box_clean_ups')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'amount_box_clean_ups'
        verbose_name = 'Amount Box Clean Up'
        verbose_name_plural = 'Amount Box Clean Ups'
        indexes = [
            models.Index(fields=['amount_box_id']),
            models.Index(fields=['box_cleanup_event_id']),
        ]

    def __str__(self):
        return f"Limpieza caja {self.id}"

    def to_domain_entity(self) -> AmountBoxCleanUpEntity:
        """Convierte a entidad de dominio"""
        return AmountBoxCleanUpEntity(
            id=self.id,
            amount_box_id=self.amount_box.id,
            total_amount=self.total_amount,
            box_cleanup_event_id=self.box_cleanup_event.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, amount_box_clean_up_entity: AmountBoxCleanUpEntity) -> 'AmountBoxCleanUp':
        """Crea desde entidad de dominio"""
        return cls(
            id=amount_box_clean_up_entity.id,
            amount_box_id=amount_box_clean_up_entity.amount_box_id,
            total_amount=amount_box_clean_up_entity.total_amount,
            box_cleanup_event_id=amount_box_clean_up_entity.box_cleanup_event_id,
            created_at=amount_box_clean_up_entity.created_at,
            updated_at=amount_box_clean_up_entity.updated_at
        )

class BoxCleanUpEvent(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='cleanup_events')
    total_amount = models.IntegerField()  # en centavos
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'box_cleanup_events'
        verbose_name = 'Box Clean Up Event'
        verbose_name_plural = 'Box Clean Up Events'
        indexes = [
            models.Index(fields=['user_id']),
        ]
    def to_domain_entity(self) -> BoxCleanUpEventEntity:
        """Convierte a entidad de dominio"""
        return BoxCleanUpEventEntity(
            id=self.id,
            total_amount=self.total_amount,
            user_id=self.user.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, box_clean_up_event_entity: BoxCleanUpEventEntity) -> 'BoxCleanUpEvent':
        """Crea desde entidad de dominio"""
        return cls(
            id=box_clean_up_event_entity.id,
            total_amount=box_clean_up_event_entity.total_amount,
            user_id=box_clean_up_event_entity.user_id,
            created_at=box_clean_up_event_entity.created_at,
            updated_at=box_clean_up_event_entity.updated_at
        )

    def __str__(self):
        return f"Evento limpieza {self.id}"

class BoxCleanUpDetail(models.Model):
    box_cleanup_event = models.ForeignKey(BoxCleanUpEvent, on_delete=models.CASCADE, related_name='details')
    box = models.ForeignKey('Box', on_delete=models.CASCADE, related_name='cleanup_details')
    amount = models.IntegerField()  # en centavos
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'box_cleanup_details'
        verbose_name = 'Box Clean Up Detail'
        verbose_name_plural = 'Box Clean Up Details'
        indexes = [
            models.Index(fields=['box_cleanup_event']),
            models.Index(fields=['box_id']),
        ]
    def __str__(self):
        return f"Limpieza caja {self.box_cleanup_event.id} - {self.amount}"
    
    def to_domain_entity(self) -> BoxCleanUpDetailEntity:
        """Convierte a entidad de dominio"""
        return BoxCleanUpDetailEntity(
            id=self.id,
            box_cleanup_event_id=self.box_cleanup_event.id,
            box_id=self.box.id,
            amount=self.amount,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, box_clean_up_detail_entity: BoxCleanUpDetailEntity) -> 'BoxCleanUpDetail':
        """Crea desde entidad de dominio"""
        return cls(
            id=box_clean_up_detail_entity.id,
            box_cleanup_event_id=box_clean_up_detail_entity.box_cleanup_event_id,
            box_id=box_clean_up_detail_entity.box_id,
            amount=box_clean_up_detail_entity.amount,
            created_at=box_clean_up_detail_entity.created_at,
            updated_at=box_clean_up_detail_entity.updated_at
        )

class TransactionType(models.Model):
    """Modelo Django para TransactionType"""
    
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'transaction_types'
        verbose_name = 'Transaction Type'
        verbose_name_plural = 'Transaction Types'
        indexes = [
            models.Index(fields=['name']),
        ]
    
    def __str__(self):
        return f"{self.name}"
    
    def to_domain_entity(self) -> TransactionTypeEntity:
        """Convierte a entidad de dominio"""
        return TransactionTypeEntity(
            id=self.id,
            name=self.name,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, transaction_type_entity: TransactionTypeEntity) -> 'TransactionType':
        """Crea desde entidad de dominio"""
        return cls(
            id=transaction_type_entity.id,
            name=transaction_type_entity.name,
            created_at=transaction_type_entity.created_at,
            updated_at=transaction_type_entity.updated_at
        )
        
class CleanUpSchedule(models.Model):
    """Modelo Django para CleanUpSchedule"""
    user = models.ForeignKey('User', on_delete=models.CASCADE, related_name='clean_up_schedules')
    clean_up_day_interval = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'clean_up_schedules'
        verbose_name = 'Clean Up Schedule'
        verbose_name_plural = 'Clean Up Schedules'
        indexes = [
            models.Index(fields=['user_id']),
        ]
        
    def __str__(self):
        return f"Programación de limpieza {self.id} - {self.user.username}"
    
    def to_domain_entity(self) -> CleanUpScheduleEntity:
        """Convierte a entidad de dominio"""
        return CleanUpScheduleEntity(
            id=self.id,
            user_id=self.user.id,
            clean_up_day_interval=self.clean_up_day_interval,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, clean_up_schedule_entity: CleanUpScheduleEntity) -> 'CleanUpSchedule':
        """Crea desde entidad de dominio"""
        return cls(
            id=clean_up_schedule_entity.id,
            user_id=clean_up_schedule_entity.user_id,
            clean_up_day_interval=clean_up_schedule_entity.clean_up_day_interval,
            created_at=clean_up_schedule_entity.created_at,
            updated_at=clean_up_schedule_entity.updated_at
        )

class SavingBoxAmountBoxTransaction(models.Model):
    """Modelo Django para SavingBoxAmountBoxTransaction"""
    saving_box = models.ForeignKey('SavingBox', on_delete=models.CASCADE, related_name='amount_box_transactions')
    amount = models.IntegerField()  # en centavos
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, related_name='saving_box_amount_box_transactions')
    amount_box = models.ForeignKey('AmountBox', on_delete=models.CASCADE, related_name='saving_box_amount_box_transactions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'saving_box_amount_box_transactions'
        verbose_name = 'Saving Box Amount Box Transaction'
        verbose_name_plural = 'Saving Box Amount Box Transactions'
        indexes = [
            models.Index(fields=['saving_box']),
            models.Index(fields=['amount_box']),
            models.Index(fields=['transaction_type']),
        ]
        
    def __str__(self):
        return f"Transacción de caja de ahorro {self.saving_box.id} - {self.amount}"
    
    def to_domain_entity(self) -> SavingBoxAmountBoxTransactionEntity:
        """Convierte a entidad de dominio"""
        return SavingBoxAmountBoxTransactionEntity(
            id=self.id,
            saving_box_id=self.saving_box.id,
            amount=self.amount,
            transaction_type_id=self.transaction_type.id,
            amount_box_id=self.amount_box.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, saving_box_amount_box_transaction_entity: SavingBoxAmountBoxTransactionEntity) -> 'SavingBoxAmountBoxTransaction':
        """Crea desde entidad de dominio"""
        return cls(
            id=saving_box_amount_box_transaction_entity.id,
            saving_box_id=saving_box_amount_box_transaction_entity.saving_box_id,
            amount=saving_box_amount_box_transaction_entity.amount,
            transaction_type_id=saving_box_amount_box_transaction_entity.transaction_type_id,
            amount_box_id=saving_box_amount_box_transaction_entity.amount_box_id,
            created_at=saving_box_amount_box_transaction_entity.created_at,
            updated_at=saving_box_amount_box_transaction_entity.updated_at
        )

class SavingBoxBoxTransaction(models.Model):
    """Modelo Django para SavingBoxBoxTransaction"""
    saving_box = models.ForeignKey('SavingBox', on_delete=models.CASCADE, related_name='box_transactions')
    amount = models.IntegerField()  # en centavos
    box = models.ForeignKey('Box', on_delete=models.CASCADE, related_name='saving_box_box_transactions')
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, related_name='saving_box_box_transactions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'saving_box_box_transactions'
        verbose_name = 'Saving Box Box Transaction'
        verbose_name_plural = 'Saving Box Box Transactions'
        indexes = [
            models.Index(fields=['saving_box']),
            models.Index(fields=['box']),
        ]
        
    def __str__(self):
        return f"Transacción de caja de ahorro {self.saving_box.id} - {self.amount}"
    
    def to_domain_entity(self) -> SavingBoxBoxTransactionEntity:
        """Convierte a entidad de dominio"""
        return SavingBoxBoxTransactionEntity(
            id=self.id,
            saving_box_id=self.saving_box.id,
            amount=self.amount,
            box_id=self.box.id,
            transaction_type_id=self.transaction_type.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, saving_box_box_transaction_entity: SavingBoxBoxTransactionEntity) -> 'SavingBoxBoxTransaction':
        """Crea desde entidad de dominio"""
        return cls(
            id=saving_box_box_transaction_entity.id,
            saving_box_id=saving_box_box_transaction_entity.saving_box_id,
            amount=saving_box_box_transaction_entity.amount,
            box_id=saving_box_box_transaction_entity.box_id,
            transaction_type_id=saving_box_box_transaction_entity.transaction_type_id,
            created_at=saving_box_box_transaction_entity.created_at,
            updated_at=saving_box_box_transaction_entity.updated_at
        )

class BoxTransaction(models.Model):
    """Modelo Django para BoxTransaction"""
    box = models.ForeignKey('Box', on_delete=models.CASCADE, related_name='transactions')
    amount = models.IntegerField()  # en centavos
    transaction_type = models.ForeignKey('TransactionType', on_delete=models.CASCADE, related_name='box_transactions')
    created_at = models.DateTimeField()
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'box_transactions'
        verbose_name = 'Transacción de caja'
        verbose_name_plural = 'Transacciones de cajas'
        ordering = ['-created_at']

    def to_domain_entity(self) -> BoxTransactionEntity:
        """Convierte a entidad de dominio"""
        return BoxTransactionEntity(
            id=self.id,
            box_id=self.box.id,
            amount=self.amount,
            transaction_type_id=self.transaction_type.id,
            created_at=self.created_at,
            updated_at=self.updated_at
        )
    
    @classmethod
    def from_domain_entity(cls, box_transaction_entity: BoxTransactionEntity) -> 'BoxTransaction':
        """Crea desde entidad de dominio"""
        return cls(
            id=box_transaction_entity.id,
            box_id=box_transaction_entity.box_id,
            amount=box_transaction_entity.amount,
            transaction_type_id=box_transaction_entity.transaction_type_id,
            created_at=box_transaction_entity.created_at,
            updated_at=box_transaction_entity.updated_at
        )