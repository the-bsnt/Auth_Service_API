from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *
from django import forms
from django.contrib.auth.forms import UserCreationForm


class CustomUserCreationForm(UserCreationForm):
    model = CustomUser
    fields = ["username", "email", "password1", "password2", "role"]


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    model = CustomUser
    list_display = ("username", "email", "is_staff", "is_active", "role")
    fieldsets = UserAdmin.fieldsets + (("Roles", {"fields": ("role",)}),)

    add_fieldsets = (
        (
            "Add User",
            {"fields": ("username", "email", "password1", "password2", "role")},
        ),
    )


admin.site.register(CustomUser, CustomUserAdmin)
