#!/bin/bash

# Exit on any error
set -e

echo "[DEBUG] $@"
if [ "$DEBUG" = "true" ]; then
    python manage.py migrate --no-input
    python manage.py collectstatic --no-input
fi

# Run server
gunicorn app.wsgi:application "$@"
