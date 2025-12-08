from django.conf import settings
from drf_yasg.views import get_schema_view


SchemaView = get_schema_view(
    info=settings.OPEN_API_INFO,
    public=True,
)


redoc_view = SchemaView.with_ui('redoc')
swagger_view = SchemaView.with_ui('swagger')
schema_format_view = SchemaView.without_ui()
