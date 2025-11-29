#!/bin/bash

# Exit on any error
set -e


function is_debug_mode() {
    # app/settings.py의 DEBUG 는 truthy falsy 값을 허용하므로,
    # 해당 파싱 방식이 반영될 수 있도록 app/settings.py에서 직접 DEBUG 값을 관측.
    echo 'from django.conf import settings; exit(0 if settings.DEBUG else 1);' \
        | python manage.py shell --no-imports
    return $?
}


function debug_init() {
    echo "[ENTRYPOINT] Running in DEBUG mode."

    python manage.py migrate --no-input
    python manage.py collectstatic --no-input || true
}


function main() {
    echo "[ENTRYPOINT] $@"

    if is_debug_mode; then
        debug_init
    fi

    # Run server
    gunicorn app.wsgi:application "$@"
}


main "$@"
