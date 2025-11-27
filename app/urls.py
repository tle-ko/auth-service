"""
URL configuration for app project.

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
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
import app.views


urlpatterns = [
    # Service Status
    # - `HEALTHCHECK` support for Docker Container
    path('health/', app.views.HealthCheckAPIView.as_view()),
]

if settings.DEBUG:
    urlpatterns += [
        path('admin/', admin.site.urls),

        # Swagger Support
        path(r'swagger/', app.views.schema.with_ui('swagger')),
        path(r'swagger/(?P<format>\.json|\.yaml)',
             app.views.schema.without_ui()),

        # Serve static files only in development
        *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
    ]
