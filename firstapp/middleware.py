from django.conf import settings
from django.http import HttpResponse


class RequestBodyLimitMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        content_length = request.META.get("CONTENT_LENGTH")
        if content_length:
            try:
                body_size = int(content_length)
            except ValueError:
                return HttpResponse("Invalid content length.", status=400)

            if body_size > settings.MAX_REQUEST_BODY_BYTES:
                return HttpResponse("Request body is too large.", status=413)

        return self.get_response(request)
