# goScanAPI_django/celery.py
import os
from celery import Celery

# Establecer la variable de entorno para Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'goScanAPI_django.settings')

# Crear la instancia de Celery
app = Celery('goScanAPI_django')

# Configurar Celery desde settings de Django
app.config_from_object('django.conf:settings', namespace='CELERY')

# Descubrir tareas automáticamente
app.autodiscover_tasks()

# Importar tareas específicas para asegurar que se registren
import infrastructure.tasks.task