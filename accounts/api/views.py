from django.contrib.auth import get_user_model
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser, AllowAny
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from ..models import Librarian, Member
from .permissions import IsAdminOrLibrarian
from .serializers import (
    MemberSerializer,
    CreateMemberSerializer,
    LibrarianSerializer,
    CreateLibrarianSerializer,
    PublicMemberRegistrationSerializer,
)


User = get_user_model()


class MemberViewset(ModelViewSet):
    queryset = Member.objects.select_related("user").all()
    permission_classes = [IsAdminOrLibrarian]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateMemberSerializer
        return MemberSerializer

    def perform_destroy(self, instance):
        instance.user.delete()
        return super().perform_destroy(instance)


class LibrarianViewset(ModelViewSet):
    queryset = Librarian.objects.select_related("user").all()
    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "create":
            return CreateLibrarianSerializer
        return LibrarianSerializer

    def perform_destroy(self, instance):
        instance.user.delete()
        return super().perform_destroy(instance)


@api_view(["POST"])
@permission_classes([AllowAny])
def register_member(request):
    """
    Public endpoint for member registration.
    Allows anyone to create a member account.
    """
    serializer = PublicMemberRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        member = serializer.save()
        return Response(
            {
                "message": "Member registered successfully",
                "member_id": member.id,
                "membership_code": member.membership_code,
                "username": member.user.username,
                "email": member.user.email,
            },
            status=status.HTTP_201_CREATED,
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
