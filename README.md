# TLE Auth Service

이 저장소는 TLE의 인증을 위한 서비스 개발이 이루어지는 곳입니다.

TLE Auth Service는 사용자의 인증(JWT)부터, 회원가입, 그 외 기능들을 제공합니다.

Django 프레임워크와 Django REST Framework를 기반으로 구축되었으며, Swagger UI를 통해 API 문서화가 이루어져 있습니다.

> 서비스 구동 시 `DEBUG` 환경변수를 `1`로 설저아여 개발용으로 배포할 경우, 일부 Endpoint가 추가되어 Django 관리자 페이지와 Swagger UI에 접근할 수 있게 됩니다.

## 개발 환경 설정

### 사전 요구사항

서비스 구동을 위해 다음의 의존성이 필요합니다:

-   Docker
-   Docker Compose

### Secrets 준비

-   `<REPO_DIR>/.secrets/secret_key.txt` 에 사용자 비밀번호 및 JWT 인코딩을 위한 `SECRET_KEY`를 작성합니다.
-   `<REPO_DIR>/.secrets/postgres_password.txt` 에 데이터베이스 비밀번호를 작성합니다.

위 두 값 모두 임의로 변경하는 것이 가능하며, 변경하는 것이 보안적으로 더 우수합니다.

### 로컬에 배포

```bash
docker compose -f docker-compose.develop.yml up -w
```

위 명령을 실행하여 Postgres 데이터베이스와 auth service를 로컬호스트에 배포합니다.

Compose 구성에서 포트포워딩은 내부 8000 -> 외부 80번으로 매핑되어 있으므로 기존 세팅을 유지할 경우 http://localhost 에 접속하여 서비스에 엑세스 할 수 있습니다.

혹은 docker-compose.develop.yml 의 `service.auth-service.ports` 를 수정하여 포트포워드 대상 포트를 변경할 수 있습니다.


## 여담

TLE 서비스의 모놀리식 아키텍쳐를 MSA로 전환하기 위해 첫 번째로 생성하는 서비스입니다.

JWT: Claim에 사용자 정보를 담아 `SECRET_KEY`로 암호화 하여 생성된 JWT 토큰을 사용자 클라이언트에 저장하고, 이 정보를 다른 마이크로서비스에서 복호화하여 참조할 수 있도록 설계되었습니다.
