from django.contrib import admin


class UsersAdmin(admin.ModelAdmin):
    list_filter = ['email', 'username']
