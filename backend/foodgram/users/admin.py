from django.contrib import admin
from .models import User


class UsersAdmin(admin.ModelAdmin):
    list_filter = ['email', 'username']
