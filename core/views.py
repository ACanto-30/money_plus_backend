from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from drf_spectacular.utils import extend_schema

# Create your views here.

@extend_schema(
    tags=['test'],
    summary='Vista de prueba',
    description='Vista simple para probar drf-spectacular'
)
class TestView(APIView):
    """Vista de prueba para diagnosticar problemas con drf-spectacular"""
    
    @extend_schema(
        responses={
            200: {
                'description': 'Respuesta exitosa',
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'status': {'type': 'string'}
                }
            }
        }
    )
    def get(self, request):
        """Endpoint de prueba GET"""
        return Response({
            'message': 'Vista de prueba funcionando correctamente',
            'status': 'success'
        }, status=status.HTTP_200_OK)
    
    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'test_data': {'type': 'string'}
                }
            }
        },
        responses={
            200: {
                'description': 'Respuesta exitosa',
                'type': 'object',
                'properties': {
                    'message': {'type': 'string'},
                    'received_data': {'type': 'string'}
                }
            }
        }
    )
    def post(self, request):
        """Endpoint de prueba POST"""
        test_data = request.data.get('test_data', 'No data provided')
        return Response({
            'message': 'Datos recibidos correctamente',
            'received_data': test_data
        }, status=status.HTTP_200_OK)
