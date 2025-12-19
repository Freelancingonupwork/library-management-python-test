from django.contrib.auth import get_user_model
from rest_framework.serializers import ModelSerializer, ValidationError
from rest_framework import serializers

from ..models import Librarian, Member


class UserSerializer(ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)
    
    class Meta:
        model = get_user_model()
        fields = ("id", "username", "password", "email", "first_name", "last_name")
        extra_kwargs = {
            "password": {"write_only": True},
        }


class CreateMemberSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("user",)

    def save(self, **kwargs):
        user = self.validated_data["user"]
        self.instance = Member.objects.create_member(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )
        return self.instance


class MemberSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("id", "membership_code", "user")


class CreateLibrarianSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Member
        fields = ("user",)

    def create(self, validated_data):
        user = validated_data["user"]
        return Librarian.objects.create_librarian(
            username=user["username"],
            password=user["password"],
            email=user["email"],
            first_name=user["first_name"],
            last_name=user["last_name"],
        )


class LibrarianSerializer(ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Librarian
        fields = ("id", "staff_code", "user")


class PublicMemberRegistrationSerializer(serializers.Serializer):
    """Serializer for public member registration"""
    username = serializers.CharField(required=True, max_length=150)
    password = serializers.CharField(required=True, write_only=True, min_length=8)
    password_confirm = serializers.CharField(required=True, write_only=True, min_length=8)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=False, allow_blank=True, max_length=150)
    last_name = serializers.CharField(required=False, allow_blank=True, max_length=150)

    def validate(self, attrs):
        if attrs["password"] != attrs["password_confirm"]:
            raise ValidationError({"password": "Passwords do not match."})
        return attrs

    def validate_email(self, value):
        User = get_user_model()
        if User.objects.filter(email=value).exists():
            raise ValidationError("A user with this email already exists.")
        return value

    def validate_username(self, value):
        User = get_user_model()
        if User.objects.filter(username=value).exists():
            raise ValidationError("A user with this username already exists.")
        return value

    def create(self, validated_data):
        password = validated_data.pop("password")
        validated_data.pop("password_confirm")
        
        # Create member (which will also create the user)
        member = Member.objects.create_member(
            username=validated_data["username"],
            password=password,
            email=validated_data["email"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
        )
        
        return member
