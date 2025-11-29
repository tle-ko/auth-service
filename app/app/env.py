"""
환경 변수와 관련된 기능 혹은 유틸리티 모음.
"""

import os
from pathlib import Path
from typing import Optional

import dotenv


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
