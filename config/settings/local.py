from .base import *
import environ

env = environ.Env()
env.read_env(BASE_DIR / ".envs/.env")

DEBUG = env.bool("DEBUG")

SECRET_KEY = env.str("SECRET_KEY")

ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

INSTALLED_APPS += ["debug_toolbar"]

# PostgreSQL configuration
# Make sure PostgreSQL is running and database/user are created
# See POSTGRESQL_SETUP.md for setup instructions
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": env("DB_NAME"),
        "USER": env("DB_USER"),
        "PASSWORD": env("DB_PASSWORD"),
        "HOST": env("DB_HOST", default="localhost"),
        "PORT": env("DB_PORT"),
    }
}

# SQLite fallback (uncomment if PostgreSQL is not available)
# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.sqlite3",
#         "NAME": BASE_DIR / "db.sqlite3",
#     }
# }

CELERY_BROKER_URL = env.str("CELERY_BROKER_URL")
