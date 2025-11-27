from django.http import HttpRequest
from django.http import HttpResponse
from django.views.decorators.http import require_http_methods
from drf_yasg.openapi import Contact
from drf_yasg.openapi import Info
from drf_yasg.views import get_schema_view
from rest_framework.permissions import AllowAny


schema = get_schema_view(
    info=Info(
        title="Time Limit Exceeded :: Authentication API",
        default_version='1.0.0',
        description="",
        contact=Contact(email="202115064@sangmyung.kr"),
    ),
    public=True,
    permission_classes=[AllowAny],
)


@require_http_methods(["GET"])
def health(request: HttpRequest):
    return HttpResponse(status=200)
