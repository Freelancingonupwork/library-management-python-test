from django.contrib import admin

# Customize Django Admin Site
admin.site.site_header = "Library Management System"
admin.site.site_title = "Library Management System"
admin.site.index_title = "Library Management System Administration"

# Unregister Auth Token from Django Admin
# This file is imported in config/urls.py to ensure it runs
try:
    from rest_framework.authtoken.models import Token
    # Check if registered before trying to unregister
    if admin.site.is_registered(Token):
        admin.site.unregister(Token)
except (admin.sites.NotRegistered, ImportError):
    pass  # Token was not registered or authtoken not installed

