from django.urls import path
from .views import *

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register_user"),
    path("login/", LoginUser.as_view(), name="login_user"),
    path("test/", send_email_otp, name="test_mail"),
]
