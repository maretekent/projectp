#!/usr/bin/env bash
set -e
python manage.py migrate --no-input

python manage.py collectstatic --no-input --verbosity 2

exec gunicorn --bind=0.0.0.0:80 configuration.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload