from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    email = models.EmailField(verbose_name="email", unique=True)
    Roles = [
        ("TEACHER", "teacher"),
        ("STUDENT", "student"),
    ]
    role = models.CharField(choices=Roles, default="STUDENT")

    # to authenticate via both email and username
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username
