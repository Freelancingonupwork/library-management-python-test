from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from rest_framework.permissions import IsAuthenticated

from accounts.api.permissions import IsAdminOrLibrarian, IsMemberOrAdminOrLibrarian
from accounts.models import Member
from ..models import BorrowedBook
from .serializers import BorrowedBookSerializer, BorrowedBookCreateSerializer


class BorrowedBookViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = BorrowedBook.objects.select_related("book_item").all()
    permission_classes = [IsMemberOrAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action in ("create"):
            return BorrowedBookCreateSerializer
        return BorrowedBookSerializer

    def get_permissions(self):
        """
        Allow members to create and view their own borrows.
        Only admin/librarian can delete (return books).
        """
        if self.action == "create":
            # Members can create borrow records
            return [IsMemberOrAdminOrLibrarian()]
        elif self.action == "destroy":
            # Only admin/librarian can delete (return books)
            return [IsAdminOrLibrarian()]
        else:
            # Members can view their own borrows, admin/librarian can view all
            return [IsMemberOrAdminOrLibrarian()]

    def get_queryset(self):
        """
        Members can only see their own borrows.
        Admin/Librarian can see all borrows.
        """
        queryset = BorrowedBook.objects.select_related("book_item", "borrower__user").all()
        
        # Check if user is authenticated
        if not self.request.user or not self.request.user.is_authenticated:
            return BorrowedBook.objects.none()
        
        # If user is admin or librarian, return all
        if self.request.user.is_staff:
            return queryset
        
        # Check if user is librarian
        from accounts.models import Librarian
        if Librarian.objects.filter(user=self.request.user).exists():
            return queryset
        
        # If user is member, return only their borrows
        try:
            member = Member.objects.get(user=self.request.user)
            return queryset.filter(borrower=member)
        except Member.DoesNotExist:
            return BorrowedBook.objects.none()

    def perform_create(self, serializer):
        """
        Automatically set the borrower to the current user's member profile
        if they are a member.
        """
        # Check if user is authenticated
        if not self.request.user or not self.request.user.is_authenticated:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must be authenticated to borrow books.")
        
        # If user is admin/librarian, they can specify borrower in request
        if self.request.user.is_staff:
            serializer.save()
            return
        
        # Check if user is librarian
        from accounts.models import Librarian
        if Librarian.objects.filter(user=self.request.user).exists():
            serializer.save()
            return
        
        # If user is member, automatically set borrower to their member profile
        try:
            member = Member.objects.get(user=self.request.user)
            serializer.save(borrower=member)
        except Member.DoesNotExist:
            # This shouldn't happen due to permission check, but handle it
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You must be a registered member to borrow books.")
