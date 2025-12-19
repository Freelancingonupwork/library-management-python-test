from rest_framework.permissions import BasePermission, SAFE_METHODS
from accounts.models import Librarian, Member


class IsAdminOrLibrarian(BasePermission):
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if Librarian.objects.filter(user=request.user).exists():
            return True
        return False


class IsMember(BasePermission):
    """Permission class to check if user is a member"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        return Member.objects.filter(user=request.user).exists()


class IsMemberOrAdminOrLibrarian(BasePermission):
    """Permission class that allows members, admins, and librarians"""
    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if Librarian.objects.filter(user=request.user).exists():
            return True
        if Member.objects.filter(user=request.user).exists():
            return True
        return False


class IsMemberOrReadOnly(BasePermission):
    """Permission class that allows members to read and create, but only admin/librarian to modify"""
    def has_permission(self, request, view):
        # Allow read operations for everyone (including anonymous)
        if request.method in SAFE_METHODS:
            return True
        
        # Allow create for authenticated members
        if request.method == "POST":
            if request.user.is_authenticated:
                if request.user.is_staff:
                    return True
                if Librarian.objects.filter(user=request.user).exists():
                    return True
                if Member.objects.filter(user=request.user).exists():
                    return True
            return False
        
        # Allow modify/delete only for admin/librarian
        if not request.user or not request.user.is_authenticated:
            return False
        if request.user.is_staff:
            return True
        if Librarian.objects.filter(user=request.user).exists():
            return True
        return False
