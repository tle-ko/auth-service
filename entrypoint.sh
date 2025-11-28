#!/bin/bash


function debug_init() {
    echo "[ENTRYPOINT] Running in DEBUG mode."

    python manage.py migrate --no-input
    python manage.py collectstatic --no-input
}


function main() {
    echo "[ENTRYPOINT] $@"

    # Exit on any error
    set -e

    # Check if DEBUG mode is enabled
    echo 'from django.conf import settings; exit(0 if settings.DEBUG else 1);' \
        | python manage.py shell --no-imports \
        && debug_init

    # Run server
    gunicorn app.wsgi:application "$@"
}


main "$@"
