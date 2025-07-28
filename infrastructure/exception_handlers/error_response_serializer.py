from django.http import JsonResponse

class ProblemDetailsErrorResponseSerializer:
    def serialize_and_send(self, request, errors: dict, title: str, status_code: int, instance: str):
        response = JsonResponse({
            "title": title,
            "status": status_code,
            "instance": instance,
            "errors": errors
        })
        response.status_code = status_code
        response["Content-Type"] = "application/problem+json; charset=utf-8"
        return response