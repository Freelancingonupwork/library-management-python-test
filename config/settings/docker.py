from .base import *
import environ

env = environ.Env()
env.read_env(BASE_DIR / ".envs/.env.dev")

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# PostgreSQL configuration for Docker
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="db"),  # Docker service name
        "PORT": env("DB_PORT"),
    }
}

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")

