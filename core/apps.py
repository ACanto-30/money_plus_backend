from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'
    
    def ready(self):
        """Se ejecuta cuando la app está lista"""
        # Importar los modelos para que Django los reconozca
        import infrastructure.persistence.models
