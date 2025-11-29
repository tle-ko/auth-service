#!/bin/bash

# Exit on any error
set -e


function main() {
    echo "[ENTRYPOINT] Arguments: $@"

    wait_for_db

    if is_debug_mode; then
        debug_init
    fi

    # Run server
    gunicorn app.wsgi:application "$@"
}


function debug_init() {
    echo "[ENTRYPOINT] Running in DEBUG mode."

    python manage.py migrate --no-input

    # 관리자 페이지, Swagger UI가 설치되어 있으므로, 항상 collect할 static 파일이 존재하는 것으로 가정.
    python manage.py collectstatic --no-input
}



function is_debug_mode() {
    # app/settings.py의 DEBUG 는 truthy falsy 값을 허용하므로,
    # 해당 파싱 방식이 반영될 수 있도록 app/settings.py에서 직접 DEBUG 값을 관측.
    echo 'from django.conf import settings; exit(0 if settings.DEBUG else 1);' \
        | python manage.py shell --no-imports
}


function wait_for_db() {
    local retries=30
    local wait=2
    echo "[ENTRYPOINT] Waiting for database to be ready..."
    for i in $(seq 1 $retries); do
        if python manage.py migrate --plan > /dev/null 2>&1; then
            echo "[ENTRYPOINT] Database is ready."
            return 0
        fi
        echo "[ENTRYPOINT] Database not ready yet (attempt $i/$retries), waiting $wait seconds..."
        sleep $wait
    done
    echo "[ENTRYPOINT] Database not ready after $((retries * wait)) seconds, exiting."
    exit 1
}


main "$@"
