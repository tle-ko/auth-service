#!/bin/bash

if curl --silent --fail http://localhost:8000/health/ > /dev/null; then
    exit 0
else
    exit 1
fi
