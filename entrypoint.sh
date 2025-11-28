#!/bin/bash

echo "[ENTRYPOINT] $@"

# Exit on any error
set -e

if [ "$DEBUG" = "true" ]; then
    python manage.py collectstatic --no-input
fi

# Run server
gunicorn app.wsgi:application "$@"
