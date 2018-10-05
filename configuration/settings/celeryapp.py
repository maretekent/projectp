from __future__ import absolute_import
import os
from structlog import get_logger
from celery import Celery
from django.conf import settings

logger = get_logger("Payment API").bind(action="Test-connection-to-rabbitmq-broker")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "configuration.settings.development")

try:
    app = Celery("Celery-paymentapi-app")
    app.config_from_object("django.conf:settings")
    app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

    broker_url = app.conf.get("BROKER_URL", None)
    broker_domain_name = None

    if broker_url:
        broker_domain_name = broker_url.split("@")[1]

    logger.info("rabbitmq-connection-started")
    logger.info(
        "rabbitmq-connection-success",
        message="rabbitmq broker connection "
        "successful to domain {0}".format(str(broker_domain_name)),
    )
except Exception as e:
    logger.exception(
        "rabbitmq-connection-error",
        message="failed to connect to rabbitmq broker with domain name {0}".format(
            str(broker_domain_name)
        ),
        error=str(e),
    )
