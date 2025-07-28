"""
URL configuration for goScanAPI_django project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView
from django.http import JsonResponse

def custom_404(request, exception):
    return JsonResponse({
        "success": False,
        "status": 404,
        "title": "Not Found",
        "instance": request.build_absolute_uri(),
        "errors": ["El recurso que solicitaste no existe."]
    }, status=404)

def custom_500(request):
    return JsonResponse({
        "success": False,
        "status": 500,
        "title": "Internal Server Error",
        "instance": request.build_absolute_uri(),
        "errors": ["Ocurrió un error interno en el servidor."]
    }, status=500)

handler404 = 'goScanAPI_django.urls.custom_404'
handler500 = 'goScanAPI_django.urls.custom_500'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('core.urls')),  # Incluye las URLs de la app core
    path('api/404/', custom_404, name='custom_404'),
    path('api/500/', custom_500, name='custom_500'),
    # Documentación de la API
    path('api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('api/docs/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('api/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),

]
