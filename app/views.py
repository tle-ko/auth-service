from django.db import connections
from django.db.utils import OperationalError
from django.http import HttpRequest
from django.http import HttpResponse
from drf_yasg.openapi import Contact
from drf_yasg.openapi import Info
from drf_yasg.utils import swagger_auto_schema
from drf_yasg.views import get_schema_view
from rest_framework import status
from rest_framework.exceptions import APIException
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView


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


class HealthCheckAPIView(APIView):
    """
    Health Check API

    배포된 컨테이너의 상태 검사를 위한 endpoint.
    컨테이너가 정상적으로 구동되었으면 200 OK를 반환한다.
    """
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: "Container is healthy.",
        }
    )
    def get(self, request: HttpRequest):
        # Database Conectivity Check
        try:
            connection = connections['default']
            connection.cursor()  # 연결 시도
        except OperationalError:
            raise APIException("Database connection failed.")

        return HttpResponse(status=status.HTTP_200_OK)
