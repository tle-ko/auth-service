"""
환경 변수와 관련된 기능 혹은 유틸리티 모음.
"""

import os
from pathlib import Path
from typing import Optional

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
