"""
환경 변수와 관련된 기능 혹은 유틸리티 모음.
"""

import json
import os
import warnings
from pathlib import Path
from typing import Any, Optional, Union

import dotenv

# Define truthy and falsy values
_TRUTHY_VALUES = ('true', '1', 't', 'y', 'yes', 'on')
_FALSY_VALUES = ('false', '0', 'f', 'n', 'no', 'off')


def load(dotenv_path: Optional[Path] = None):
    """.env 파일이 있다면 .env 파일에서 환경 변수를 로드합니다.

    Args:
        dotenv_path: .env 파일 경로 (기본값: None)
    """
    # Load .env file if it exists
    if (dotenv_path is not None) and dotenv_path.exists():
        dotenv.load_dotenv(dotenv_path=dotenv_path, override=True)


def get(key: str, default: Optional[str] = None, required: bool = False, strip: bool = True, blank: bool = False) -> Optional[str]:
    """환경 변수 값을 가져옵니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)
        strip: 값의 앞뒤 공백 제거 여부 (기본값: True)
        blank: 빈 문자열 허용 여부 (False일 때 빈 문자열은 None으로 간주)

    Returns:
        환경 변수 값 또는 기본값

    Raises:
        ValueError: required=True이고 환경 변수가 설정되지 않은 경우
    """
    string_value = os.getenv(key, default)

    if strip and (string_value is not None):
        string_value = string_value.strip()

    if not blank and (string_value == ''):
        string_value = None

    if required and (string_value is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return string_value


def get_bool(key: str, default: Optional[bool] = None, strip: bool = True, required: bool = False) -> Optional[bool]:
    """환경 변수를 불린 값으로 파싱합니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        strip: 앞뒤 공백 제거 여부 (기본값: True)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        불린 값 또는 기본값

    Raises:
        ValueError: 잘못된 불린 값이거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    raw_value = os.getenv(key)
    boolean_value = default

    if raw_value is not None:
        if _is_truthy(raw_value, strip=strip):
            boolean_value = True
        elif _is_falsy(raw_value, strip=strip):
            boolean_value = False
        else:
            raise ValueError(
                f'Environment variable "{key}" has invalid boolean value.'
            )

    if required and (boolean_value is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return boolean_value


def get_json(key: str, default: Optional[Any] = None, required: bool = False) -> Optional[Any]:
    """환경 변수 값을 JSON으로 파싱하여 반환하거나 기본값을 반환합니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        JSON으로 파싱된 값 또는 기본값

    Raises:
        ValueError: 환경 변수 값이 올바른 JSON이 아니거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    raw_value = os.getenv(key)
    json_value = default

    if raw_value is not None:
        try:
            json_value = json.loads(raw_value)
        except ValueError as e:
            raise ValueError(
                f'Environment variable "{key}" has invalid JSON value.'
            ) from e

    if required and (json_value is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return json_value


def get_path(key: str, default: Optional[Path] = None, required: bool = False, relative_to: Optional[Union[Path, str]] = None) -> Optional[Path]:
    """환경 변수에 지정된 파일 경로를 Path 객체로 반환합니다.

    Args:
        key: 파일 경로가 저장된 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)
        relative_to: 파일 탐색을 허용할 최상위 경로.
            이 값이 None이면 모든 경로가 허용됩니다.
            (기본값: None)

    Returns:
        파일 경로 또는 기본값

    Raises:
        ValueError: 환경 변수 값이 유효하지 않거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    raw_path = os.getenv(key)
    path = default

    if raw_path is not None:
        try:
            path = Path(raw_path).resolve()
        except OSError as e:
            raise ValueError(
                f'Environment variable "{key}" has invalid file path.'
            ) from e

    # 파일 경로가 허용 탐색 범위 이내인지 검사
    if relative_to and (path is not None):
        try:
            relative_to_path = Path(relative_to).resolve()
        except OSError as e:
            raise ValueError(
                f'Environment variable "{key}" has invalid "relative_to" path.'
            ) from e

        # 디렉토리인지 검증
        if not relative_to_path.is_dir():
            raise ValueError(
                f'"relative_to" path for environment variable "{key}" is not a directory.'
            )

        try:
            path.relative_to(relative_to_path)
        except ValueError:
            raise ValueError(
                f'Path specified in environment variable "{key}" is outside '
                f'the allowed directory "{relative_to_path}".'
            )

    if required and (path is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return path


def get_file_content(key: str, default: Optional[str] = None, required: bool = False, strip: bool = True, blank: bool = False, relative_to: Optional[Union[Path, str]] = None, encoding: str = 'utf-8') -> Optional[str]:
    """환경 변수에 지정된 파일 경로의 내용을 읽어옵니다.

    .. deprecated::
        이 함수는 deprecated 되었습니다.
        대신 직접 Path().resolve(), is_relative_to(), read_text()를 사용하세요.

    Args:
        key: 파일 경로가 저장된 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)
        strip: 값의 앞뒤 공백 제거 여부 (기본값: True)
        blank: 파일 내용에 대하여 빈 문자열 허용 여부 (False일 때 빈 문자열은 None으로 간주)
        relative_to: 파일 탐색을 허용할 최상위 경로.
            이 값이 None이면 모든 경로가 허용됩니다.
            (기본값: None)
        encoding: 파일 인코딩 (기본값: 'utf-8')

    Returns:
        파일 내용 또는 기본값

    Raises:
        ValueError: 파일을 읽을 수 없거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    warnings.warn(
        'get_file_content() is deprecated. '
        'Use Path().resolve(), is_relative_to(), and read_text() directly in settings.py instead.',
        DeprecationWarning,
        stacklevel=2
    )
    raw_path = os.getenv(key)
    content = default

    if raw_path is not None:
        try:
            path = Path(raw_path).resolve()
        except OSError as e:
            raise ValueError(
                f'Environment variable "{key}" has invalid file path.'
            ) from e

        # 파일 경로가 허용 탐색 범위 이내인지 검사
        if relative_to is not None:
            relative_to_path = Path(relative_to).resolve()
            try:
                if not relative_to_path.is_dir():
                    raise ValueError
                path.relative_to(relative_to_path)
            except ValueError:
                raise ValueError(
                    f'Path specified in environment variable "{key}" is outside '
                    f'the allowed directory, or the "relative_to" path is not a directory.'
                )

        # 파일 내용 읽어오기
        fread_error_msg = None

        try:
            content = path.read_text(encoding=encoding)
        except FileNotFoundError:
            fread_error_msg = f'File specified in environment variable "{key}" not found.'
        except PermissionError:
            fread_error_msg = f'Permission denied to read file specified in environment variable "{key}".'
        except OSError:
            fread_error_msg = f'Error reading file specified in environment variable "{key}".'
        except UnicodeDecodeError:
            fread_error_msg = f'Error decoding file specified in environment variable "{key}" with encoding "{encoding}".'
        except Exception:
            fread_error_msg = f'Unexpected error while reading file specified in environment variable "{key}".'

        if fread_error_msg:
            raise ValueError(fread_error_msg)

    if strip and (content is not None):
        content = content.strip()

    if not blank and (content == ''):
        content = None

    if required and (content is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return content


def _is_truthy(value: Optional[str], strip: bool = True) -> bool:
    """문자열이 참 값인지 확인합니다.

    Args:
        value: 확인할 문자열
        strip: 앞뒤 공백 제거 여부 (기본값: True)

    Returns:
        참 값 여부 (true, 1, t, y, yes, on 중 하나인 경우 True)
    """
    if strip and (value is not None):
        value = value.strip()

    if value is None:
        return False

    return value.lower() in _TRUTHY_VALUES


def _is_falsy(value: Optional[str], strip: bool = True) -> bool:
    """문자열이 거짓 값인지 확인합니다.

    Args:
        value: 확인할 문자열
        strip: 앞뒤 공백 제거 여부 (기본값: True)

    Returns:
        거짓 값 여부 (false, 0, f, n, no, off 중 하나인 경우 True)
    """
    if strip and (value is not None):
        value = value.strip()

    if value is None:
        return False

    return value.lower() in _FALSY_VALUES
