"""
환경 변수와 관련된 기능 혹은 유틸리티 모음.
"""

import json
import os
from dotenv import load_dotenv
from pathlib import Path
from typing import Dict, Iterable, List, Optional, Union


TRUTHY_VALUES = ('true', '1', 't', 'y', 'yes', 'on')
FALSY_VALUES = ('false', '0', 'f', 'n', 'no', 'off')


JSON_SCALAR = Union[str, int, float, bool, None]
JSON = Union[Dict[str, 'JSON'], List['JSON'], JSON_SCALAR]


load_dotenv()


def get(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """환경 변수 값을 가져옵니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        환경 변수 값 또는 기본값

    Raises:
        ValueError: required=True이고 환경 변수가 설정되지 않은 경우
    """
    value = os.getenv(key)
    retval = default

    if value is not None:
        retval = value.strip()

    if required and (retval is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return retval


def get_json(key: str, default: Optional[JSON] = None, required: bool = False) -> Optional[JSON]:
    value = os.getenv(key)
    retval = default

    if value is not None:
        try:
            retval = json.loads(value)
        except json.JSONDecodeError:
            raise ValueError(
                f'Environment variable "{key}" has invalid JSON value.'
            )

    if required and (retval is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return retval


def get_bool(key: str, default: Optional[bool] = None, required: bool = False) -> Optional[bool]:
    """환경 변수를 불린 값으로 파싱합니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        불린 값 또는 기본값

    Raises:
        ValueError: 잘못된 불린 값이거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    value = os.getenv(key)
    retval = default

    if value is not None:
        if is_truthy(value):
            retval = True
        elif is_falsy(value):
            retval = False
        else:
            raise ValueError(
                f'Environment variable "{key}" has invalid boolean value.'
            )

    if required and (retval is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return retval


def get_int(key: str, default: Optional[int] = None, required: bool = False) -> Optional[int]:
    """환경 변수를 정수 값으로 파싱합니다.

    Args:
        key: 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        정수 값 또는 기본값

    Raises:
        ValueError: 잘못된 정수 값이거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    value = os.getenv(key)
    retval = default

    if value is not None:
        try:
            retval = int(value)
        except ValueError:
            raise ValueError(
                f'Environment variable "{key}" has invalid integer value.'
            )

    if required and (retval is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return retval


def get_file_content(key: str, default: Optional[str] = None, required: bool = False) -> Optional[str]:
    """환경 변수에 지정된 파일 경로의 내용을 읽어옵니다.

    Args:
        key: 파일 경로가 저장된 환경 변수 이름
        default: 기본값 (환경 변수가 없을 때 반환)
        required: 필수 여부 (True일 때 환경 변수가 없으면 예외 발생)

    Returns:
        파일 내용 또는 기본값

    Raises:
        ValueError: 파일을 찾을 수 없거나 required=True이고 환경 변수가 설정되지 않은 경우
    """
    value = os.getenv(key)
    retval = default

    if value is not None:
        try:
            retval = Path(value).read_text().strip()
        except FileNotFoundError:
            raise ValueError(
                f'Environment variable "{key}" has invalid file path.'
            )

    if required and (retval is None):
        raise ValueError(
            f'Environment variable "{key}" is required but not set.'
        )

    return retval


def is_truthy(value: Optional[str]) -> bool:
    """문자열이 참 값인지 확인합니다.

    Args:
        value: 확인할 문자열

    Returns:
        참 값 여부 (true, 1, t, y, yes, on 중 하나인 경우 True)
    """
    return _is_one_of(value, TRUTHY_VALUES)


def is_falsy(value: Optional[str]) -> bool:
    """문자열이 거짓 값인지 확인합니다.

    Args:
        value: 확인할 문자열

    Returns:
        거짓 값 여부 (false, 0, f, n, no, off 중 하나인 경우 True)
    """
    return _is_one_of(value, FALSY_VALUES)


def _is_one_of(value: Optional[str], iterable: Iterable[str], case_insensitive: bool = True) -> bool:
    """문자열이 주어진 값들 중 하나인지 확인합니다.

    Args:
        value: 확인할 문자열
        iterable: 비교할 값들의 컬렉션
        case_insensitive: 대소문자 구분 여부 (기본값: True)

    Returns:
        값이 컬렉션에 포함되어 있는지 여부

    Raises:
        TypeError: value가 문자열이 아닌 경우
    """
    if value is None:
        return False
    if not isinstance(value, str):
        raise TypeError(f'Expected str, got {type(value).__name__}')
    if case_insensitive:
        value = value.strip().lower()
    return value in iterable
