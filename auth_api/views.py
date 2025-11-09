from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from rest_framework.exceptions import ValidationError, PermissionDenied, NotFound
from .serializers import CustomTokenObtainPairSerializer, VerifyOTPSerializer
from .models import PendingUser

from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from .tokens import CustomRefreshToken
from django.contrib.auth import get_user_model
from django.conf import settings


User = get_user_model()


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


# to verify opt sent while registering user
class VerifyOTPView(APIView):
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = VerifyOTPSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get("email")
            otp = serializer.data.get("otp")
            pending_user_instance = PendingUser.objects.filter(
                email=email, otp=otp, is_verified=False
            ).last()

            if not pending_user_instance:
                raise ValidationError("Error: Invalid OTP or OTP Expired!!!")
            try:
                user = User.objects.create_user(
                    username=pending_user_instance.username,
                    email=pending_user_instance.email,
                    role=pending_user_instance.role,
                    password=pending_user_instance.password,
                )
            except:
                return Response(
                    {"detail": "The User is already registered in the system."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            user.save()

            refresh = CustomRefreshToken.for_user(user)
            return Response(
                {
                    "message": "OTP successfully verified. Registering User Successfully",
                    "tokens": {
                        "refresh": str(refresh),
                        "access": str(refresh.access_token),
                    },
                },
                status=status.HTTP_202_ACCEPTED,
            )


def send_email_otp(validated_user_data):
    # if PendingUser.objects.get(email__iexact= validated_user_data['email'])
    otp_instance = PendingUser.objects.create(**validated_user_data)

    email = validated_user_data.get("email")
    print(email)
    print(settings.EMAIL_HOST_USER)
    subject = "Your One-Time Password (OTP) for User Registration"
    message = f"""Dear {otp_instance.username.upper()},

Thank you for registering user on our learning platform.

To complete this action, please use the One-Time Password (OTP) provided below:

Your OTP: {otp_instance.otp}

This OTP is valid for the next 5 minutes and can only be used once. Please do not share this OTP with anyone for security reasons.

If you did not initiate this request, please ignore this email.


Sincerely,

The Scholars Portal Team
"""
    try:
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email],
            fail_silently=False,
        )
    except Exception as e:
        return Response({"error": f"Error sending otp: {e}"}, status=500)
