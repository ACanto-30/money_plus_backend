from celery import shared_task
from django.utils import timezone
from domain.ports.secondary.password_reset_repositoy import IPasswordResetRepository

@shared_task
def cleanup_expired_password_resets():
    """Limpia códigos de reseteo expirados cada 10 minutos"""
    try:
        # Importar aquí para evitar imports circulares
        from infrastructure.configuration.container import Container
        
        # Usar el repositorio para mantener arquitectura hexagonal
        password_reset_repo = Container.resolve(IPasswordResetRepository)
        
        # Obtener códigos expirados
        expired_codes = password_reset_repo.get_expired_codes()
        print(f"Encontrados {len(expired_codes)} códigos expirados")
        
        # Marcar como usados
        invalidated_count = 0
        for code in expired_codes:
            try:
                password_reset_repo.invalidate_code(code.code)
                invalidated_count += 1
                print(f"Invalidado código: {code.code} para usuario: {code.user_id}")
            except Exception as e:
                print(f"Error invalidando código {code.code}: {str(e)}")
        
        print(f"Limpieza completada: {invalidated_count} códigos expirados marcados")
        return f"Limpieza completada: {invalidated_count} códigos expirados marcados"
        
    except Exception as e:
        print(f"Error en limpieza de códigos expirados: {str(e)}")
        return f"Error: {str(e)}" 