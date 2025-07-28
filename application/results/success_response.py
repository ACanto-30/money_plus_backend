from typing import Any
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import status
from application.abstractions.success_response import ISuccessResponse

class SuccessResponse(ISuccessResponse):
    """
    Implementación concreta de respuesta exitosa con formato consistente
    """
    
    def __init__(self, title: str, data: Any, instance: str):
        """
        Inicializa una nueva respuesta exitosa
        
        Args:
            title: Título descriptivo de la operación
            data: Datos de la respuesta
            instance: Identificador de trazabilidad (instance)
        """
        self._title = title
        self._data = data
        self._instance = instance
    
    @property
    def title(self) -> str:
        """Título descriptivo de la operación"""
        return self._title
    
    @property
    def data(self) -> Any:
        """Datos de la respuesta"""
        return self._data
    
    @property
    def trace_identifier(self) -> str:
        """Identificador de trazabilidad"""
        return self._instance
    
    def to_response(self) -> Response:
        """
        Convierte la respuesta exitosa a un Response de DRF con formato consistente
        siguiendo el mismo patrón que ProblemDetailsErrorResponseSerializer
        
        Returns:
            Response con el formato estándar de la API
        """
        response_data = {
            'title': self._title,
            'status': 200,
            'instance': self._instance,
            'data': self._data
        }
        
        response = JsonResponse(response_data)
        response.status_code = 200
        # No cambiamos el Content-Type para respuestas exitosas
        return response 