from django.contrib import admin
from accounts.models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'last_name', 'login', 'password', 'organization']


admin.site.register(User, UserAdmin)