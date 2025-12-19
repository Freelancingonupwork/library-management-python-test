from django.urls import path, include
from rest_framework_nested.routers import DefaultRouter, NestedDefaultRouter

from .api.views import BookViewset, AuthorViewset, BookItemViewSet
from .views import books_list_view, book_detail_view, borrow_book_view


router = DefaultRouter()
router.register("books", BookViewset, basename="books")
router.register("authors", AuthorViewset, basename="authors")

books_router = NestedDefaultRouter(router, "books", lookup="book")
books_router.register("items", BookItemViewSet, basename="book-items")

urlpatterns = [
    # HTML pages (must come before API routes)
    path("books/", books_list_view, name="library-books-list"),
    path("books/<int:book_id>/", book_detail_view, name="library-book-detail"),
    path("books/<int:book_id>/borrow/", borrow_book_view, name="library-borrow-book"),
    # API endpoints
    path("api/", include(router.urls)),
    path("api/", include(books_router.urls)),
]
