from django.test import TestCase, override_settings
from rest_framework import status


class DocEndpointsDebugModeTestCase(TestCase):
    """DEBUG=True일 때 문서 엔드포인트 접근 가능 여부 테스트"""

    @override_settings(DEBUG=True)
    def test_swagger_ui_accessible_in_debug_mode(self):
        """DEBUG 모드에서 Swagger UI 접근 가능"""
        response = self.client.get('/doc/swagger/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(DEBUG=True)
    def test_redoc_ui_accessible_in_debug_mode(self):
        """DEBUG 모드에서 ReDoc UI 접근 가능"""
        response = self.client.get('/doc/redoc/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(DEBUG=True)
    def test_schema_json_accessible_in_debug_mode(self):
        """DEBUG 모드에서 스키마 JSON 접근 가능"""
        response = self.client.get('/doc/swagger.json/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    @override_settings(DEBUG=True)
    def test_schema_yaml_accessible_in_debug_mode(self):
        """DEBUG 모드에서 스키마 YAML 접근 가능"""
        response = self.client.get('/doc/swagger.yaml/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class DocEndpointsProductionModeTestCase(TestCase):
    """DEBUG=False일 때 문서 엔드포인트 접근 제한 테스트"""

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_swagger_ui_not_accessible_in_production(self):
        """프로덕션 모드에서 Swagger UI 접근 불가"""
        response = self.client.get('/doc/swagger/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_redoc_ui_not_accessible_in_production(self):
        """프로덕션 모드에서 ReDoc UI 접근 불가"""
        response = self.client.get('/doc/redoc/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_schema_json_not_accessible_in_production(self):
        """프로덕션 모드에서 스키마 JSON 접근 불가"""
        response = self.client.get('/doc/swagger.json/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    @override_settings(DEBUG=False, ALLOWED_HOSTS=['testserver'])
    def test_schema_yaml_not_accessible_in_production(self):
        """프로덕션 모드에서 스키마 YAML 접근 불가"""
        response = self.client.get('/doc/swagger.yaml/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
