from django.test import TestCase


class HealthCheckAPIViewTest(TestCase):
    def test_get_200(self):
        """
        GET /health/ 요청 시 200 OK를 반환하는지 테스트.
        """
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)
