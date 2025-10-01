from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import AllowAny

class HealthCheckView(APIView):
    """View para verificar el estado de la API"""
    permission_classes = [AllowAny]

    @extend_schema(
        request={
            'application/json': {
                'type': 'object',
                'properties': {
                    'status': {'type': 'string'}
                },
                'required': ['status']
            }
        },
        responses={
            200: {
                'description': 'API funcionando correctamente',
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean'},
                    'status': {'type': 'integer'},
                    'instance': {'type': 'string'},
                    'title': {'type': 'string'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'status': {'type': 'string'}
                        }
                    }
                }
            }
        }
    )
    def get(self, request):
        """Verifica el estado de la API"""
        return Response({
            'success': True,
            'status': 200,
            'instance': 'http://localhost:8000/api/health-check',
            'title': 'API funcionando correctamente',
            'data': {
                'status': 'OK'
            }
        })