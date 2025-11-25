#!/bin/bash

./manage.py migrate --no-input
./manage.py runserver 0.0.0.0:8000
