from django.contrib import admin
from django.urls import path, include
from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

# Import admin configuration to unregister models
# This ensures Token is unregistered after all apps load their admin
import config.admin

urlpatterns = [
    path("admin/", admin.site.urls),
    path("auth/", include("dj_rest_auth.urls")),
    path("account/", include("accounts.urls")),  # HTML pages: /account/login, /account/register
    path("accounts/", include("accounts.urls")),  # API endpoints: /accounts/members/, etc.
    path("library/", include("library.urls")),
    path("reservation/", include("reservation.urls")),
    path("borrowing/", include("borrowing.urls")),
    path("fines/", include("fines.urls")),
    path("__debug__/", include("debug_toolbar.urls")),
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]
