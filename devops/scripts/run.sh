#!/usr/bin/env bash
set -e

python manage.py migrate --no-input

python manage.py collectstatic --no-input --verbosity 2

echo "from django.contrib.auth.models import User; User.objects.filter(username='$DEV_LOGIN_USERNAME').exists() or User.objects.create_superuser('$DEV_LOGIN_USERNAME', '$DEV_LOGIN_EMAIL', '$DEV_LOGIN_PASSWORD')" | python manage.py shell --settings=$DJANGO_SETTINGS_MODULE

exec gunicorn --bind=0.0.0.0:80 configuration.wsgi --workers=5 --log-level=info --log-file=---access-logfile=- --error-logfile=- --timeout 30000 --reload