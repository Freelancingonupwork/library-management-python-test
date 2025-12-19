from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import AllowAny, IsAuthenticatedOrReadOnly

from ..models import Book, BookItem, Author
from accounts.api.permissions import IsMemberOrReadOnly, IsAdminOrLibrarian
from .filters import AuthorFilter, BookFilter, BookItemFilter
from .serializers import (
    BookSerializer,
    BookCreateUpdateSerializer,
    AuthorSerializer,
    AuthorListSerializer,
    BookItemSerializer,
    BookItemCreateUpdateSerializer,
)


class BookViewset(ModelViewSet):
    queryset = Book.objects.prefetch_related("author").all()
    filterset_class = BookFilter
    permission_classes = [IsMemberOrReadOnly]

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BookCreateUpdateSerializer
        return BookSerializer

    def get_permissions(self):
        """
        Allow anyone to read (list/retrieve), but only admin/librarian to create/update/delete
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]  # Allow anonymous users to browse books
        return [IsAdminOrLibrarian()]  # Only admin/librarian can modify


class AuthorViewset(ModelViewSet):
    filterset_class = AuthorFilter
    permission_classes = [IsMemberOrReadOnly]

    def get_queryset(self):
        if self.action == "list":
            Author.objects.prefetch_related("books").all()
        return Author.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return AuthorListSerializer
        return AuthorSerializer

    def get_permissions(self):
        """
        Allow anyone to read (list/retrieve), but only admin/librarian to create/update/delete
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]  # Allow anonymous users to browse authors
        return [IsAdminOrLibrarian()]  # Only admin/librarian can modify


class BookItemViewSet(ModelViewSet):
    filterset_class = BookItemFilter
    permission_classes = [IsMemberOrReadOnly]

    def get_queryset(self):
        return (
            BookItem.objects
                .select_related("book")
                .prefetch_related("book__author")
                .filter(book=self.kwargs["book_pk"])
        )

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return BookItemCreateUpdateSerializer
        return BookItemSerializer

    def get_serializer_context(self):
        return {"book_id": self.kwargs["book_pk"]}

    def get_permissions(self):
        """
        Allow anyone to read (list/retrieve), but only admin/librarian to create/update/delete
        """
        if self.action in ["list", "retrieve"]:
            return [AllowAny()]  # Allow anonymous users to browse book items
        return [IsAdminOrLibrarian()]  # Only admin/librarian can modify