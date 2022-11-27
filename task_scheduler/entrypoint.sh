#!/bin/sh

python manage.py makemigrations

exec "$@"