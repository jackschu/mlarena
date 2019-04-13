from django.contrib import admin
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser

from django.contrib.auth.admin import UserAdmin


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm

#admin.site.register(CustomUser, CustomUserAdmin)
