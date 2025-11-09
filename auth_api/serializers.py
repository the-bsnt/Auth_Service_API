from rest_framework import serializers
from rest_framework_simplejwt.serializers import (
    TokenObtainPairSerializer,
)
from django.contrib.auth import authenticate
from .models import PendingUser
from datetime import timedelta
from django.utils import timezone


# customizin the TokenObtainPairSerializer
class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    # customizing validate method to authenticate user via both email and password
    def validate(self, attrs):
        user_identifier = attrs.get(self.username_field)
        password = attrs.get("password")
        user = authenticate(
            request=self.context.get("request"),
            username=user_identifier,
            password=password,
        )
        if not user:
            raise serializers.ValidationError("Invalid Credentials")
        refresh = self.get_token(user)
        data = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return data

    # method to add extra claims in the token
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token["email"] = user.email
        token["role"] = user.role
        return token


# serializer to verify the otp send while registering user
class VerifyOTPSerializer(serializers.Serializer):
    email = serializers.EmailField()
    otp = serializers.CharField(max_length=6)
    # is_expired = serializers.SerializerMethodField(read_only=True)

    # class Meta:
    #     model = PendingUser
    #     fields = ["email", "otp", "is_expired"]
    # def get_is_expired(self,obj):
    #     if timezone.now() > obj.created_at + timedelta(minutes=5):
    #         return False
