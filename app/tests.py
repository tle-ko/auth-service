import os
from django.core.files.temp import NamedTemporaryFile
from django.test import TestCase
from app import env


class HealthCheckAPIViewTest(TestCase):
    def test_get_200(self):
        """
        GET /health/ 요청 시 200 OK를 반환하는지 테스트.
        """
        response = self.client.get('/health/')
        self.assertEqual(response.status_code, 200)


class EnvModuleTest(TestCase):
    def setUp(self):
        # 테스트 전 환경 변수 초기화
        self.test_keys = ['TEST_VAR', 'TEST_ARRAY',
                          'TEST_BOOL', 'TEST_INT', 'TEST_FILE']
        for key in self.test_keys:
            if key in os.environ:
                del os.environ[key]

    def tearDown(self):
        # 테스트 후 환경 변수 정리
        for key in self.test_keys:
            if key in os.environ:
                del os.environ[key]

    def test_get_existing_value(self):
        os.environ['TEST_VAR'] = 'test_value'
        result = env.get('TEST_VAR')
        self.assertEqual(result, 'test_value')

    def test_get_default_value(self):
        result = env.get('TEST_VAR', 'default_value')
        self.assertEqual(result, 'default_value')

    def test_get_none_when_not_set(self):
        result = env.get('TEST_VAR')
        self.assertIsNone(result)

    def test_get_required_raises_error(self):
        with self.assertRaises(ValueError) as cm:
            env.get('TEST_VAR', required=True)
        self.assertIn('required but not set', str(cm.exception))

    def test_get_array_existing_value(self):
        os.environ['TEST_ARRAY'] = 'a,b,c'
        result = env.get_array('TEST_ARRAY')
        self.assertEqual(result, ['a', 'b', 'c'])

    def test_get_array_with_spaces(self):
        os.environ['TEST_ARRAY'] = ' a , b , c '
        result = env.get_array('TEST_ARRAY')
        self.assertEqual(result, ['a', 'b', 'c'])

    def test_get_array_empty_items(self):
        os.environ['TEST_ARRAY'] = 'a,,b,'
        result = env.get_array('TEST_ARRAY')
        self.assertEqual(result, ['a', 'b'])

    def test_get_array_default_value(self):
        result = env.get_array('TEST_ARRAY', ['default'])
        self.assertEqual(result, ['default'])

    def test_get_array_required_raises_error(self):
        with self.assertRaises(ValueError):
            env.get_array('TEST_ARRAY', required=True)

    def test_get_bool_truthy_values(self):
        truthy_values = ['true', '1', 't', 'y', 'yes', 'on', 'TRUE', 'True']
        for value in truthy_values:
            os.environ['TEST_BOOL'] = value
            result = env.get_bool('TEST_BOOL')
            self.assertTrue(result, f'Failed for value: {value}')

    def test_get_bool_falsy_values(self):
        falsy_values = ['false', '0', 'f', 'n', 'no', 'off', 'FALSE', 'False']
        for value in falsy_values:
            os.environ['TEST_BOOL'] = value
            result = env.get_bool('TEST_BOOL')
            self.assertFalse(result, f'Failed for value: {value}')

    def test_get_bool_invalid_value(self):
        os.environ['TEST_BOOL'] = 'invalid'
        with self.assertRaises(ValueError) as cm:
            env.get_bool('TEST_BOOL')
        self.assertIn('invalid boolean value', str(cm.exception))

    def test_get_bool_default_value(self):
        result = env.get_bool('TEST_BOOL', True)
        self.assertTrue(result)

    def test_get_bool_required_raises_error(self):
        with self.assertRaises(ValueError):
            env.get_bool('TEST_BOOL', required=True)

    def test_get_int_valid_value(self):
        os.environ['TEST_INT'] = '42'
        result = env.get_int('TEST_INT')
        self.assertEqual(result, 42)

    def test_get_int_negative_value(self):
        os.environ['TEST_INT'] = '-10'
        result = env.get_int('TEST_INT')
        self.assertEqual(result, -10)

    def test_get_int_invalid_value(self):
        os.environ['TEST_INT'] = 'not_a_number'
        with self.assertRaises(ValueError) as cm:
            env.get_int('TEST_INT')
        self.assertIn('invalid integer value', str(cm.exception))

    def test_get_int_default_value(self):
        result = env.get_int('TEST_INT', 100)
        self.assertEqual(result, 100)

    def test_get_int_required_raises_error(self):
        with self.assertRaises(ValueError):
            env.get_int('TEST_INT', required=True)

    def test_get_file_content_valid_file(self):
        with NamedTemporaryFile(mode='w', delete=False) as f:
            f.write('test content')
            temp_path = f.name
        try:
            os.environ['TEST_FILE'] = temp_path
            result = env.get_file_content('TEST_FILE')
            self.assertEqual(result, 'test content')
        finally:
            os.unlink(temp_path)

    def test_get_file_content_invalid_file(self):
        os.environ['TEST_FILE'] = '/nonexistent/file.txt'
        with self.assertRaises(ValueError) as cm:
            env.get_file_content('TEST_FILE')
        self.assertIn('invalid file path', str(cm.exception))

    def test_get_file_content_default_value(self):
        result = env.get_file_content('TEST_FILE', 'default content')
        self.assertEqual(result, 'default content')

    def test_get_file_content_required_raises_error(self):
        with self.assertRaises(ValueError):
            env.get_file_content('TEST_FILE', required=True)

    def test_is_truthy_valid_values(self):
        truthy_values = ['true', '1', 't', 'y', 'yes', 'on']
        for value in truthy_values:
            self.assertTrue(env.is_truthy(value))
            self.assertTrue(env.is_truthy(value.upper()))

    def test_is_truthy_invalid_values(self):
        invalid_values = ['false', '0', 'invalid', None]
        for value in invalid_values:
            self.assertFalse(env.is_truthy(value))

    def test_is_falsy_valid_values(self):
        falsy_values = ['false', '0', 'f', 'n', 'no', 'off']
        for value in falsy_values:
            self.assertTrue(env.is_falsy(value))
            self.assertTrue(env.is_falsy(value.upper()))

    def test_is_falsy_invalid_values(self):
        invalid_values = ['true', '1', 'invalid', None]
        for value in invalid_values:
            self.assertFalse(env.is_falsy(value))
