import os
from unittest.mock import patch
from pathlib import Path

from django.conf import settings
from django.core.files.temp import NamedTemporaryFile
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


class GetBoolTest(TestCase):
    def test_parses_truthy_values(self):
        """다양한 참 값 문자열을 True로 파싱하는지 확인한다.

        대소문자 구분 없이 'true', '1', 't', 'y', 'yes', 'on'을 True로 인식해야 한다.
        """
        for value in ('true', '1', 't', 'y', 'yes', 'on', 'TRUE', 'True', 'YES'):
            with self.subTest(value=value):
                with patch.dict(os.environ, {'BOOL_VAR': value}):
                    self.assertTrue(env.get_bool('BOOL_VAR'))

    def test_parses_falsy_values(self):
        """다양한 거짓 값 문자열을 False로 파싱하는지 확인한다.

        대소문자 구분 없이 'false', '0', 'f', 'n', 'no', 'off'를 False로 인식해야 한다.
        """
        for value in ('false', '0', 'f', 'n', 'no', 'off', 'FALSE', 'False', 'NO'):
            with self.subTest(value=value):
                with patch.dict(os.environ, {'BOOL_VAR': value}):
                    self.assertFalse(env.get_bool('BOOL_VAR'))

    @patch.dict(os.environ, {}, clear=True)
    def test_default_parameter(self):
        """환경 변수가 설정되지 않았을 때 default 파라미터 값을 반환하는지 확인한다.

        default가 없으면 None을 반환한다.
        """
        self.assertIsNone(env.get_bool('MISSING_VAR'))
        self.assertTrue(env.get_bool('MISSING_VAR', default=True))
        self.assertFalse(env.get_bool('MISSING_VAR', default=False))

    @patch.dict(os.environ, {}, clear=True)
    def test_required_parameter(self):
        """필수 환경 변수가 설정되지 않았을 때 ValueError를 발생시키는지 확인한다."""
        with self.assertRaises(ValueError):
            env.get_bool('REQUIRED_VAR', required=True)

    @patch.dict(os.environ, {'BOOL_VAR': 'invalid'})
    def test_raises_for_invalid_value(self):
        """불린으로 파싱할 수 없는 값에 대해 ValueError를 발생시키는지 확인한다.

        보안상 잘못된 값을 조용히 무시하지 않고 명시적으로 에러를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR')

    @patch.dict(os.environ, {'BOOL_VAR': ''})
    def test_raises_for_empty_string(self):
        """빈 문자열에 대해 ValueError를 발생시키는지 확인한다.

        빈 문자열을 False로 해석하면 보안 문제가 발생할 수 있으므로 에러를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR')

    @patch.dict(os.environ, {'BOOL_VAR': '  true  '})
    def test_strip_parameter(self):
        """공백이 포함된 불린 값에서 strip 파라미터 동작을 확인한다.

        기본적으로 strip=True이므로 앞뒤 공백을 제거하고 파싱한다.
        strip=False로 설정하면 공백을 유지하여 파싱에 실패한다.
        """
        self.assertTrue(env.get_bool('BOOL_VAR'))
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR', strip=False)

    @patch.dict(os.environ, {'BOOL_VAR': '   '})
    def test_raises_for_whitespace_only(self):
        """공백만 있는 값에 대해 ValueError를 발생시키는지 확인한다.

        공백 제거 후 빈 문자열이 되면 에러를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR')

    @patch.dict(os.environ, {}, clear=True)
    def test_required_with_default(self):
        """required와 default를 함께 사용할 때 default 값을 반환하는지 확인한다.

        환경 변수가 없어도 default가 있으면 required=True여도 에러가 발생하지 않는다.
        """
        self.assertTrue(
            env.get_bool('MISSING_VAR', default=True, required=True)
        )
        self.assertFalse(
            env.get_bool('MISSING_VAR', default=False, required=True)
        )

    @patch.dict(os.environ, {'BOOL_VAR': '0x1'})
    def test_raises_for_hex_value(self):
        """유사 형식의 값에 대해 ValueError를 발생시키는지 확인한다.

        보안상 '0x1', '0b1' 같은 유사 형식을 허용하지 않아야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR')

    @patch.dict(os.environ, {'BOOL_VAR': 'True1'})
    def test_raises_for_partial_match(self):
        """부분 일치 값에 대해 ValueError를 발생시키는지 확인한다.

        보안상 'True1', '1true' 같은 부분 일치를 허용하지 않아야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_bool('BOOL_VAR')

    def test_raises_for_null_like_strings(self):
        """null 유사 문자열에 대해 ValueError를 발생시키는지 확인한다.

        보안상 'null', 'none', 'undefined' 같은 값을 False로 해석하지 않아야 한다.
        """
        for value in ('null', 'none', 'undefined', 'NULL', 'None', 'UNDEFINED'):
            with self.subTest(value=value):
                with patch.dict(os.environ, {'BOOL_VAR': value}):
                    with self.assertRaises(ValueError):
                        env.get_bool('BOOL_VAR')


class GetJsonTest(TestCase):
    @patch.dict(os.environ, {'JSON_VAR': '{"key": "value"}'})
    def test_parses_dict(self):
        """JSON 객체 문자열을 딕셔너리로 파싱하는지 확인한다."""
        self.assertEqual(env.get_json('JSON_VAR'), {'key': 'value'})

    @patch.dict(os.environ, {'JSON_VAR': '[1, 2, 3]'})
    def test_parses_list(self):
        """JSON 배열 문자열을 리스트로 파싱하는지 확인한다."""
        self.assertEqual(env.get_json('JSON_VAR'), [1, 2, 3])

    @patch.dict(os.environ, {'JSON_VAR': '"string"'})
    def test_parses_string(self):
        """JSON 문자열을 파싱하는지 확인한다."""
        self.assertEqual(env.get_json('JSON_VAR'), 'string')

    @patch.dict(os.environ, {'JSON_VAR': 'null'})
    def test_parses_null(self):
        """JSON null 값을 None으로 파싱하는지 확인한다."""
        self.assertIsNone(env.get_json('JSON_VAR'))

    @patch.dict(os.environ, {'JSON_VAR': 'true'})
    def test_parses_boolean(self):
        """JSON 불린 값을 파싱하는지 확인한다."""
        self.assertTrue(env.get_json('JSON_VAR'))
        with patch.dict(os.environ, {'JSON_VAR': 'false'}):
            self.assertFalse(env.get_json('JSON_VAR'))

    @patch.dict(os.environ, {'JSON_VAR': '123'})
    def test_parses_number(self):
        """JSON 숫자 값을 파싱하는지 확인한다."""
        self.assertEqual(env.get_json('JSON_VAR'), 123)
        with patch.dict(os.environ, {'JSON_VAR': '123.45'}):
            self.assertEqual(env.get_json('JSON_VAR'), 123.45)

    @patch.dict(os.environ, {}, clear=True)
    def test_default_parameter(self):
        """환경 변수가 설정되지 않았을 때 default 파라미터 값을 반환하는지 확인한다.

        default가 없으면 None을 반환한다.
        """
        self.assertIsNone(env.get_json('MISSING_VAR'))
        self.assertEqual(env.get_json('MISSING_VAR', default={'default': True}),
                         {'default': True})

    @patch.dict(os.environ, {}, clear=True)
    def test_required_parameter(self):
        """필수 환경 변수가 설정되지 않았을 때 ValueError를 발생시키는지 확인한다."""
        with self.assertRaises(ValueError):
            env.get_json('REQUIRED_VAR', required=True)

    @patch.dict(os.environ, {'JSON_VAR': 'invalid json'})
    def test_raises_for_invalid_json(self):
        """잘못된 JSON 형식에 대해 ValueError를 발생시키는지 확인한다.

        보안상 잘못된 JSON을 조용히 무시하지 않고 명시적으로 에러를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_json('JSON_VAR')

    @patch.dict(os.environ, {'JSON_VAR': ''})
    def test_raises_for_empty_string(self):
        """빈 문자열에 대해 ValueError를 발생시키는지 확인한다.

        보안상 빈 문자열을 조용히 무시하지 않고 명시적으로 에러를 발생시켜야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_json('JSON_VAR')

    @patch.dict(os.environ, {}, clear=True)
    def test_required_with_default(self):
        """required와 default를 함께 사용할 때 default 값을 반환하는지 확인한다.

        환경 변수가 없어도 default가 있으면 required=True여도 에러가 발생하지 않는다.
        """
        self.assertEqual(env.get_json('MISSING_VAR', default={'key': 'value'}, required=True),
                         {'key': 'value'})

    @patch.dict(os.environ, {'JSON_VAR': '{"nested": {"key": [1, 2, 3]}}'})
    def test_parses_nested_structure(self):
        """중첩된 JSON 구조를 올바르게 파싱하는지 확인한다."""
        self.assertEqual(
            env.get_json('JSON_VAR'),
            {'nested': {'key': [1, 2, 3]}},
        )

    @patch.dict(os.environ, {'JSON_VAR': '{"key": null}'})
    def test_parses_null_in_object(self):
        """객체 내부의 null 값을 올바르게 파싱하는지 확인한다.

        환경 변수 자체가 null인 경우와 객체 내부에 null이 있는 경우를 구분해야 한다.
        """
        self.assertEqual(env.get_json('JSON_VAR'), {'key': None})


class GetPathTest(TestCase):
    def _create_temp_file(self) -> Path:
        """임시 파일을 생성하고 Path를 반환하는 헬퍼 함수."""
        with NamedTemporaryFile(mode='w+', delete=False) as f:
            self.addCleanup(os.unlink, f.name)
            return Path(f.name).resolve()

    @patch.dict(os.environ, {'PATH_VAR': '/tmp/test.txt'})
    def test_returns_resolved_path(self):
        """환경 변수의 경로를 resolve된 Path 객체로 반환하는지 확인한다."""
        result = env.get_path('PATH_VAR')
        self.assertIsInstance(result, Path)
        self.assertEqual(result, Path('/tmp/test.txt').resolve())

    @patch.dict(os.environ, {}, clear=True)
    def test_default_parameter(self):
        """환경 변수가 설정되지 않았을 때 default 파라미터 값을 반환하는지 확인한다."""
        self.assertIsNone(env.get_path('MISSING_VAR'))
        default_path = Path('/default/path')
        self.assertEqual(env.get_path('MISSING_VAR', default=default_path),
                         default_path)

    @patch.dict(os.environ, {}, clear=True)
    def test_required_parameter(self):
        """필수 환경 변수가 설정되지 않았을 때 ValueError를 발생시키는지 확인한다."""
        with self.assertRaises(ValueError):
            env.get_path('REQUIRED_VAR', required=True)

    def test_relative_path_resolution(self):
        """상대 경로를 절대 경로로 resolve하는지 확인한다."""
        with patch.dict(os.environ, {'PATH_VAR': './relative/path'}):
            result = env.get_path('PATH_VAR')
            self.assertTrue(result.is_absolute())

    def test_symlink_resolution(self):
        """심볼릭 링크를 실제 경로로 resolve하는지 확인한다."""
        file = self._create_temp_file()
        symlink = file.parent / 'symlink_test'
        self.addCleanup(lambda: symlink.unlink(missing_ok=True))
        symlink.symlink_to(file)
        with patch.dict(os.environ, {'PATH_VAR': str(symlink)}):
            result = env.get_path('PATH_VAR')
            self.assertEqual(result, file)

    def test_relative_to_allows_path_in_directory(self):
        """relative_to로 지정된 디렉토리 내부의 경로를 허용하는지 확인한다."""
        file = self._create_temp_file()
        with patch.dict(os.environ, {'PATH_VAR': str(file)}):
            result = env.get_path('PATH_VAR', relative_to=file.parent)
            self.assertEqual(result, file)

    def test_relative_to_rejects_path_outside_directory(self):
        """relative_to로 지정된 디렉토리 외부의 경로를 거부하는지 확인한다.

        경로 탐색 공격(path traversal)을 방지하기 위한 보안 검증이다.
        """
        file = self._create_temp_file()
        other_dir = settings.BASE_DIR / 'other_dir'
        with patch.dict(os.environ, {'PATH_VAR': str(file)}):
            with self.assertRaises(ValueError):
                env.get_path('PATH_VAR', relative_to=other_dir)

    def test_relative_to_rejects_invalid_directory(self):
        """relative_to가 디렉토리가 아닌 경우 ValueError를 발생시키는지 확인한다."""
        file = self._create_temp_file()
        with patch.dict(os.environ, {'PATH_VAR': str(file)}):
            with self.assertRaises(ValueError):
                env.get_path('PATH_VAR', relative_to=file)

    def test_relative_to_with_symlink_attack(self):
        """심볼릭 링크를 이용한 경로 탐색 공격을 방어하는지 확인한다.

        허용된 디렉토리 내부의 심볼릭 링크가 외부를 가리킬 때 이를 차단해야 한다.
        """
        file = self._create_temp_file()
        allowed_dir = file.parent / 'allowed'
        symlink = allowed_dir / 'symlink'
        # Note: LIFO 구조이므로 아래와 같이 clean up 순서를 구성해야함.
        self.addCleanup(
            lambda: allowed_dir.rmdir() if allowed_dir.exists() else None
        )
        self.addCleanup(lambda: symlink.unlink(missing_ok=True))
        allowed_dir.mkdir(exist_ok=True)
        symlink.symlink_to(file)
        with patch.dict(os.environ, {'PATH_VAR': str(symlink)}):
            with self.assertRaises(ValueError):
                env.get_path('PATH_VAR', relative_to=allowed_dir)

    @patch.dict(os.environ, {'PATH_VAR': '../../../etc/passwd'})
    def test_path_traversal_attack_prevention(self):
        """경로 탐색 공격 시도를 방어하는지 확인한다.

        상대 경로를 사용한 상위 디렉토리 접근 시도를 차단해야 한다.
        """
        with self.assertRaises(ValueError):
            env.get_path('PATH_VAR', relative_to=settings.BASE_DIR)

    @patch.dict(os.environ, {}, clear=True)
    def test_required_with_default(self):
        """required와 default를 함께 사용할 때 default 값을 반환하는지 확인한다."""
        default_path = Path('/default')
        self.assertEqual(env.get_path('MISSING_VAR', default=default_path, required=True),
                         default_path)
