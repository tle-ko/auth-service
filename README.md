# TLE Auth Service

[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-orange)](https://www.django-rest-framework.org/)

TLE(Time Limit Exceeded)의 마이크로서비스 아키텍처를 위한 인증 서비스입니다.

## 개요

-   **JWT 기반 인증**: 사용자 인증 및 토큰 관리
-   **회원가입/로그인**: 사용자 계정 관리
-   **API 문서화**: Swagger UI 제공
-   **마이크로서비스**: 다른 서비스와의 JWT 토큰 공유

## 개발 가이드

### 환경 변수

Docker compose를 사용하지 않고 직접 컨테이너를 실행할 경우 필요한 환경 변수입니다.

| 변수명            | 설명                                               | 기본값  | 필수                             |
| ----------------- | -------------------------------------------------- | ------- | -------------------------------- |
| `SECRET_KEY`      | Django 암호화 키                                   |         | `SECRET_KEY_FILE` 미설정 시 필수 |
| `SECRET_KEY_FILE` | Django 암호화 키가 저장된 파일                     |         | `SECRET_KEY` 미설정 시 필수      |
| `DEBUG`           | 디버그 모드 활성 여부                              | `False` | Optional                         |
| `ALLOWED_HOSTS`   | 허용된 호스트명 (JSON 배열, 예: `["example.com"]`) |         | 디버그 모드가 아니면 필수        |
