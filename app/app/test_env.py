import os
from unittest.mock import patch

from django.test import TestCase

from app import env


class GetTest(TestCase):
    @patch.dict(os.environ, {'TEST_VAR': 'test_value'})
    def test_returns_env_value(self):
        """환경 변수가 설정되어 있을 때 해당 값을 그대로 반환하는지 확인한다."""
        self.assertEqual(env.get('TEST_VAR'), 'test_value')

    @patch.dict(os.environ, {}, clear=True)
    def test_default_parameter(self):
        """환경 변수가 설정되지 않았을 때 default 파라미터 값을 반환하는지 확인한다.

        default가 없으면 None을 반환한다.
        """
        self.assertIsNone(env.get('MISSING_VAR'))
        self.assertEqual(env.get('MISSING_VAR', default='default'), 'default')

    @patch.dict(os.environ, {}, clear=True)
    def test_required_parameter(self):
        """필수 환경 변수가 설정되지 않았을 때 ValueError를 발생시키는지 확인한다.

        required=True로 설정하면 환경 변수가 없을 때 예외를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get('REQUIRED_VAR', required=True)

    @patch.dict(os.environ, {'STRIP_VAR': '  value  '})
    def test_strip_parameter(self):
        """환경 변수 값의 앞뒤 공백을 제거하는지 확인한다.

        기본적으로 strip=True이며, strip=False로 설정하면 공백을 유지한다.
        """
        self.assertEqual(env.get('STRIP_VAR'), 'value')
        self.assertEqual(env.get('STRIP_VAR', strip=False), '  value  ')

    @patch.dict(os.environ, {}, clear=True)
    def test_strip_applies_to_default(self):
        """환경 변수가 없어서 default 값을 사용할 때도 strip이 적용되는지 확인한다."""
        self.assertEqual(env.get('MISSING_VAR', default='  default  '),
                         'default')

    @patch.dict(os.environ, {'EMPTY_VAR': ''})
    def test_blank_parameter(self):
        """빈 문자열 환경 변수를 None으로 처리하는지 확인한다.

        기본적으로 blank=False이므로 빈 문자열은 None으로 변환된다.
        blank=True로 설정하면 빈 문자열을 그대로 반환한다.
        required와 함께 사용할 때도 blank=True면 빈 문자열을 허용한다.
        """
        self.assertIsNone(env.get('EMPTY_VAR'))
        self.assertEqual(env.get('EMPTY_VAR', blank=True), '')
        with self.assertRaises(ValueError):
            env.get('EMPTY_VAR', required=True)
        self.assertEqual(env.get('EMPTY_VAR', required=True, blank=True), '')

    @patch.dict(os.environ, {'WHITESPACE_VAR': '   '})
    def test_blank_with_whitespace(self):
        """공백만 있는 환경 변수가 strip 후 빈 문자열로 처리되는지 확인한다.

        strip이 먼저 적용되어 공백이 제거되고, 그 결과 빈 문자열이 되면 blank 처리 로직이 적용된다.
        """
        self.assertIsNone(env.get('WHITESPACE_VAR'))
        self.assertEqual(env.get('WHITESPACE_VAR', blank=True), '')

    @patch.dict(os.environ, {}, clear=True)
    def test_blank_applies_to_default(self):
        """환경 변수가 없어서 default 값을 사용할 때도 blank 처리가 적용되는지 확인한다.

        default로 빈 문자열을 제공하면 blank=False일 때 None으로 변환된다.
        """
        self.assertIsNone(env.get('MISSING_VAR', default=''))
        self.assertEqual(env.get('MISSING_VAR', default='', blank=True), '')
