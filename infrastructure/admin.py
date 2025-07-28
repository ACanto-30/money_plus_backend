from django.contrib import admin
from infrastructure.persistence.models import (
    User, Role, Box, Family, FamilyRole, FamilyMember, 
    LoanState, Loan, LoanRepayment, Session, AmountBox, AmountBoxTransaction, BoxCleanUpEvent, BoxCleanUpDetail,
    TransactionType,
)

@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'description', 'created_at']
    search_fields = ['name', 'description']
    list_filter = ['created_at']

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['username', 'email', 'role', 'created_at']
    search_fields = ['username', 'email']
    list_filter = ['role', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Box)
class BoxAdmin(admin.ModelAdmin):
    list_display = ['name', 'amount', 'is_active', 'created_at']
    search_fields = ['name']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Family)
class FamilyAdmin(admin.ModelAdmin):
    list_display = ['name', 'family_code', 'is_active', 'created_at']
    search_fields = ['name', 'family_code']
    list_filter = ['is_active', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(FamilyRole)
class FamilyRoleAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']

@admin.register(FamilyMember)
class FamilyMemberAdmin(admin.ModelAdmin):
    list_display = ['user', 'family', 'is_active', 'is_banned', 'created_at']
    search_fields = ['user__username', 'family__name']
    list_filter = ['is_active', 'is_banned', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LoanState)
class LoanStateAdmin(admin.ModelAdmin):
    list_display = ['state', 'created_at']
    search_fields = ['state']
    list_filter = ['created_at']

@admin.register(Loan)
class LoanAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'from_user', 'to_user', 'family', 'state', 'created_at']
    search_fields = ['title', 'description', 'from_user__username', 'to_user__username']
    list_filter = ['state', 'family', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(LoanRepayment)
class LoanRepaymentAdmin(admin.ModelAdmin):
    list_display = ['title', 'amount', 'loan', 'user', 'created_at']
    search_fields = ['title', 'description', 'user__username']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'client_uuid', 'is_active', 'expires_at', 'created_at']
    search_fields = ['user__username', 'client_uuid']
    list_filter = ['is_active', 'expires_at', 'created_at']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(TransactionType)
class TransactionTypeAdmin(admin.ModelAdmin):
    list_display = ['name', 'created_at']
    search_fields = ['name']
    list_filter = ['created_at']
    readonly_fields = ['created_at', 'updated_at']

