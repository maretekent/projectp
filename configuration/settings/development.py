from .base import *

DEBUG = True
ALLOWED_HOSTS = ["*"]
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql_psycopg2",
#         "NAME": os.getenv("DB_NAME"),
#         "USER": os.getenv("DB_USER"),
#         "PASSWORD": os.getenv("DB_PASSWORD"),
#         "HOST": os.getenv("DB_HOST"),
#         "PORT": os.getenv("DB_PORT"),
#     }
# }

# INSTALLED_APPS = INSTALLED_APPS + ["corsheaders", "django_extensions"]

# CORS_ORIGIN_ALLOW_ALL = True

# MIDDLEWARE = ["corsheaders.middleware.CorsMiddleware"] + MIDDLEWARE

CSRF_COOKIE_SECURE = False

configure_structlog("development")