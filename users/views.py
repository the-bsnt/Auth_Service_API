from rest_framework.views import APIView
from .models import *
from .serializers import *
from rest_framework.response import Response
from rest_framework import status
from auth_api.serializers import *
from auth_api.tokens import CustomRefreshToken
from django.contrib.auth import authenticate, hashers
from auth_api.views import send_email_otp, VerifyOTPView


class LoginUser(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            serializer = LoginSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                user = authenticate(
                    username=serializer.data["username"],
                    password=serializer.data["password"],
                )
            if user is not None:
                refresh = CustomRefreshToken.for_user(user)
                return Response(
                    {
                        "message": "User Authenticated Successfully!",
                        "tokens": {
                            "refresh": str(refresh),
                            "access": str(refresh.access_token),
                        },
                    },
                    status=status.HTTP_202_ACCEPTED,
                )
            else:
                return Response(
                    {
                        "message": "invalid credentials",
                    },
                    status=status.HTTP_403_FORBIDDEN,
                )
        except Exception as e:
            return Response(
                {"error": "An error occurred: {}".format(str(e))}, status=400
            )


class RegisterUser(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        try:
            serializer = CustomUserSerializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                # to hash the password before creating pending user instance
                # serializer.validated_data["password"] = hashers.make_password(
                #     serializer.validated_data["password"]
                # )
                send_email_otp(serializer.validated_data)
                return Response(
                    {
                        "detail": "OTP sent to your email. Please verify to complete the registration."
                    },
                    status=status.HTTP_200_OK,
                )

            return Response(serializer.errors, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response(
                {"detail": "An error occurred: {}".format(str(e))}, status=500
            )
