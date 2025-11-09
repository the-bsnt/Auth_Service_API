from django.db import models
from django.conf import settings
import random


class PendingUser(models.Model):
    username = models.CharField(unique=True)
    email = models.EmailField(unique=True)
    role = models.CharField()
    password = models.CharField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        if not self.otp:
            self.otp = str(random.randint(100000, 999999))
            super().save(*args, **kwargs)
