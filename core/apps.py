from django.apps import AppConfig


class CoreConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'core'

    def ready(self):
        # Unregister Auth Token from Django Admin
        # This runs when the app is ready, but Token might be registered later
        # So we also unregister it in config/urls.py as a backup
        from django.contrib import admin
        try:
            from rest_framework.authtoken.models import Token
            if admin.site.is_registered(Token):
                admin.site.unregister(Token)
        except (admin.sites.NotRegistered, ImportError):
            pass  # Token was not registered or authtoken not installed
