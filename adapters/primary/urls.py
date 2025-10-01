from django.urls import path
from .user_registration_view import (
    UserRegistrationView,
)

from .authentication_view import (
    RefreshRefreshToken,
)
from .user_profile_view import UserProfileView
from .user_login_view import UserLoginView
from .password_reset_view import PasswordResetView
from .authentication_view import RefreshAccessToken
from .amount_box_transaction_view import AmountBoxTransactionView
from .saving_box_transaction_view import SavingBoxTransactionView
from .clean_up_view import CleanUpView
from .box_view import BoxView, BoxCreateView
from .saving_box_view import SavingBoxView
from .saving_box_transaction_view import SavingBoxTransactionView
from .amount_box_box_transaction_view import AmountBoxBoxTransactionView
from .amount_box_view import AmountBoxView
from .box_transaction_view import BoxTransactionView
from .role_view import RoleView
from .health_check_view import HealthCheckView
urlpatterns = [
    # Rutas de usuarios
    path('users/register', UserRegistrationView.as_view(), name='user-register'),
    path('users/login', UserLoginView.as_view(), name='user-login'),
    path('users/password-reset', PasswordResetView.as_view(), name='password-reset'),
    
    # Rutas de autenticación
    path('users/profile', UserProfileView.as_view(), name='user-profile'),
    # Rutas de autenticación
    path('auth/refresh-token/refresh', RefreshRefreshToken.as_view(), name='refresh-token-refresh'),
    path('auth/access-token/refresh', RefreshAccessToken.as_view(), name='access-token-refresh'),

    path('amount-boxes/<int:amount_box_id>/transactions', AmountBoxTransactionView.as_view(), name='amount-boxes-transactions'),

    # Rutas de cajas de ahorro
    path('saving-boxes/<int:saving_box_id>/transactions', SavingBoxTransactionView.as_view(), name='saving-boxes-transactions'),
    path('saving-boxes', SavingBoxView.as_view(), name='saving-boxes'),
    path('box-clean-ups', CleanUpView.as_view(), name='clean-up'),

    path('boxes', BoxCreateView.as_view(), name='box-create'),           # Para POST (crear)
    path('boxes/<int:id>', BoxView.as_view(), name='box-view'),  # Para GET y DELETE (por id)

    # Rutas de transacciones de cajas de ahorro
    path('boxes/<int:box_id>/transactions', AmountBoxBoxTransactionView.as_view(), name='box-transactions'),

    # Rutas de cajas de dinero
    path('amount-boxes', AmountBoxView.as_view(), name='amount-boxes'),

    # Rutas de transacciones de cajas
    path('boxes/<int:box_id>/transactions/make', BoxTransactionView.as_view(), name='box-transactions-view'),

    # Rutas de roles
    path('roles', RoleView.as_view(), name='roles'),

    # Rutas de salud
    path('health-check', HealthCheckView.as_view(), name='health-check'),
]