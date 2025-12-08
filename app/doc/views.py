from django.conf import settings
from drf_yasg.views import get_schema_view
from rest_framework.permissions import BasePermission


class IsDebug(BasePermission):
    """
    Permission class that allows access only when Django's DEBUG mode is enabled.
    Useful for restricting certain endpoints to development environments.
    """
    def has_permission(self, request, view):
        return settings.DEBUG


SchemaView = get_schema_view(
    info=settings.OPEN_API_INFO,
    public=True,
)


redoc_view = SchemaView.with_ui('redoc')
swagger_view = SchemaView.with_ui('swagger')
schema_format_view = SchemaView.without_ui()
