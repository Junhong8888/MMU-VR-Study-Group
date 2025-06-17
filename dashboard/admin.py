from django.contrib import admin
from .models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'get_duration_minutes')


