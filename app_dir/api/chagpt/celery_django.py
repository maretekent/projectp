# pip install celery[redis]


# settings.py

# Celery configuration
CELERY_BROKER_URL = 'amqp://guest:guest@localhost:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'
CELERY_TIMEZONE = 'UTC'

# celery.py

import os
from celery import Celery
from django.conf import settings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'your_project.settings')

app = Celery('your_project')
app.config_from_object('django.conf:settings')
app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

# tasks.py

from celery import shared_task


@shared_task
def add(x, y):
	return x + y


# celery -A your_project worker --loglevel=info


# views.py

from .tasks import add


def my_view(request):
	result = add.delay(4, 4)
	print(result.get())

# You can also use the apply_async method to schedule the task to run at a specific time in the future or
# to provide additional options for the task.
