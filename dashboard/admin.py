from django.contrib import admin
from .models import UserSession

@admin.register(UserSession)
class UserSessionAdmin(admin.ModelAdmin):
    list_display = ('user', 'login_time', 'logout_time', 'duration_minutes')

    def duration_minutes(self, obj):
        if obj.logout_time:
            return round((obj.logout_time - obj.login_time).total_seconds() / 60, 2)
        return 0
