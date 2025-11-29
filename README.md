# TLE Auth Service

[![Docker](https://img.shields.io/badge/Docker-Ready-blue)](https://www.docker.com/)
[![Django](https://img.shields.io/badge/Django-4.x-green)](https://www.djangoproject.com/)
[![DRF](https://img.shields.io/badge/DRF-3.x-orange)](https://www.django-rest-framework.org/)

TLE(Time Limit Exceeded)의 마이크로서비스 아키텍처를 위한 인증 서비스입니다.

## 개요

-   **JWT 기반 인증**: 사용자 인증 및 토큰 관리
-   **회원가입/로그인**: 사용자 계정 관리
-   **API 문서화**: Swagger UI 제공
-   **마이크로서비스**: 다른 서비스와의 JWT 토큰 공유

### 기술 스택

-   **Backend**: Django + Django REST Framework
-   **Database**: PostgreSQL
-   **Authentication**: JWT (JSON Web Token)
-   **Documentation**: Swagger UI
-   **Containerization**: Docker + Docker Compose

> 💡 **개발 모드**: `DEBUG=1` 환경변수 설정 시 Django 관리자 페이지와 Swagger UI에 접근할 수 있습니다.

## 빠른 시작

### 사전 요구사항

-   [Docker](https://www.docker.com/get-started) 20.10+
-   [Docker Compose](https://docs.docker.com/compose/install/) 2.0+

### 1. 저장소 클론

```bash
git clone <repository-url>
cd auth-service
```

### 2. 환경 설정

보안 키 파일들을 생성합니다:

```bash
# 디렉토리 생성
mkdir -p .secrets

# JWT 서명과 데이터 암호화를 위한 비밀키 (랜덤 문자열 생성 권장)
echo "your-super-secret-key-here" > .secrets/secret_key.txt

# PostgreSQL 데이터베이스 비밀번호
echo "your-postgres-password" > .secrets/postgres_password.txt
```

> ⚠️ **보안 주의**: 실제 운영환경에서는 강력한 랜덤 키를 사용하세요.

### 3. 서비스 실행

```bash
# 개발 환경 실행
docker compose -f docker-compose.develop.yml up -d

# 로그 확인
docker compose -f docker-compose.develop.yml logs -f
```

> 💡 **개발 모드**: 개발 환경 실행 명령 옵션으로 `-w`를 추가하여 watch mode 기능을 활성화 할 수 있습니다.

### 4. 접속 확인

-   **API 서버**: http://localhost (포트 80)
-   **Health Check**: http://localhost/health/
-   **Swagger UI**: http://localhost/swagger/ (DEBUG=1일 때)
-   **Django Admin**: http://localhost/admin/ (DEBUG=1일 때)

## 테스트

### Docker 컨테이너 테스트

```bash
# Django 단위 테스트
python manage.py test
```

<!-- TODO: Docker build 및 운영 테스트 추가 -->

## 아키텍처

### 마이크로서비스 설계

TLE 서비스의 모놀리식 아키텍처를 MSA로 전환하는 첫 번째 서비스입니다.

### JWT 토큰 구조

<!-- TODO: 토큰 구조 설계하기

```json
{
  "header": {
    "alg": "HS256",
    "typ": "JWT"
  },
  "payload": {
    "user_id": 123,
    "username": "user@example.com",
    "exp": 1640995200,
    "iat": 1640908800
  }
}
```
-->

-   **서명**: `SECRET_KEY`로 HMAC SHA256 알고리즘 사용
-   **저장**: 클라이언트 측 저장 (localStorage, cookie 등)
-   **검증**: 다른 마이크로서비스에서 동일한 `SECRET_KEY`로 검증

## API 문서

<!-- TODO: 과거 모놀리식 API 호환성을 신경쓰며 재설계 하기

### 주요 엔드포인트

| Method | Endpoint          | Description         |
| ------ | ----------------- | ------------------- |
| GET    | `/health/`        | 헬스체크            |
| POST   | `/auth/login/`    | 로그인              |
| POST   | `/auth/register/` | 회원가입            |
| POST   | `/auth/refresh/`  | 토큰 갱신           |
| GET    | `/swagger/`       | API 문서 (개발모드) |

-->

자세한 API 문서는 Swagger UI에서 확인할 수 있습니다.

## 개발 가이드

### 환경 변수

Docker compose를 사용하지 않고 직접 컨테이너를 실행할 경우 필요한 환경변수 입니다.

| 변수명                   | 설명                                       | 기본값  | 필수                                                |
| ------------------------ | ------------------------------------------ | ------- | --------------------------------------------------- |
| `DEBUG`                  | 디버그 모드                                | `False` | ❌                                                  |
| `SECRET_KEY`             | Django, JWT 암호화 키                      |         | ✅ (`SECRET_KEY_FILE`이 설정되었다면 필수 X)        |
| `SECRET_KEY_FILE`        | Django, JWT 암호화 키가 저장된 파일        |         | ❌                                                  |
| `POSTGRES_HOST`          | 데이터베이스 호스트                        |         | ✅                                                  |
| `POSTGRES_PORT`          | 데이터베이스 Port                          | `5432`  | ❌                                                  |
| `POSTGRES_DB`            | 데이터베이스 이름                          |         | ✅                                                  |
| `POSTGRES_USER`          | 데이터베이스 사용자명                      |         | ✅                                                  |
| `POSTGRES_PASSWORD`      | 데이터베이스 사용자 비밀번호               |         | ✅ (`POSTGRES_PASSWORD_FILE`이 설정되었다면 필수 X) |
| `POSTGRES_PASSWORD_FILE` | 데이터베이스 사용자 비밀번호가 저장된 파일 |         | ❌                                                  |

### 포트 설정 변경

`docker-compose.develop.yml`에서 포트 매핑을 수정할 수 있습니다:

```yaml
services:
  tle-auth-service:
    ports:
      - "8080:8000"  # 외부:내부 포트
```
