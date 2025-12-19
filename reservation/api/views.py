from rest_framework.viewsets import GenericViewSet
from rest_framework import mixins
from drf_spectacular.utils import extend_schema

from accounts.api.permissions import IsAdminOrLibrarian

from ..models import ReservedBook
from .serializers import ReservedBookSerializer, ReservedBookCreateSerializer


@extend_schema(exclude=True)  # Hide from API documentation
class ReservedBookViewset(
    mixins.CreateModelMixin,
    mixins.RetrieveModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    GenericViewSet,
):
    queryset = ReservedBook.objects.select_related("book_item").all()
    permission_classes = [IsAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action in ("create"):
            return ReservedBookCreateSerializer
        return ReservedBookSerializer
