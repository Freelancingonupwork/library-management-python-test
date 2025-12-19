from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .api.views import MemberViewset, LibrarianViewset, register_member
from .views import login_view, register_view, logout_view


router = DefaultRouter()
router.register("members", MemberViewset, basename="members")
router.register("librarians", LibrarianViewset, basename="librarians")

urlpatterns = [
    # HTML pages - accessible via both /account/ and /accounts/
    path("login/", login_view, name="account-login"),
    path("login", login_view, name="account-login-no-slash"),  # Support /account/login without trailing slash
    path("register/", register_view, name="account-register"),
    path("logout/", logout_view, name="account-logout"),
    # API endpoints
    path("api/register/", register_member, name="register-member-api"),
    path("", include(router.urls)),
]