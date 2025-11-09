from rest_framework import serializers
from .models import *


class CustomUserSerializer(serializers.ModelSerializer):
    password1 = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = CustomUser
        fields = [
            "id",
            "username",
            "email",
            "role",
            "password1",
            "password2",
            "password",
        ]
        read_only_fields = [
            "password",
        ]

    def validate(self, attrs):
        psw1 = attrs.pop("password1")
        psw2 = attrs.pop("password2")
        if psw2 != psw1:
            raise serializers.ValidationError(
                {"password": "The two password fields didn't match."}
            )
        attrs["password"] = psw1
        return super().validate(attrs)

    def create(self, validated_data):
        psw = validated_data.pop("password")
        instance = super().create(validated_data)
        instance.set_password(psw)
        instance.save()
        return instance


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)
