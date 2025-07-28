from infrastructure.configuration.container import Container

class ClearScopeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        Container.clear()  # Limpia singletons y scoped después de cada request
        return response