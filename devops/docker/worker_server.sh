#!/usr/bin/env bash

celery -A configuration.settings.celeryapp flower --port=5555

# celery -A configuration.settings.celeryapp worker -E -n jumoportal-worker -Q \
#         extract_new_emails,send_new_email_task,send_out_welcome_emails \
#         --concurrency=1 \
#         --loglevel=info