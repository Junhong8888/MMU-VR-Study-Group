from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    login_time = models.DateTimeField()
    logout_time = models.DateTimeField(null=True, blank=True)

    def get_duration_minutes(self, now=None):
        if self.login_time:
            end_time = self.logout_time or (now or timezone.now())
            duration = end_time - self.login_time
            return int(duration.total_seconds() // 60)
        return 0
    get_duration_minutes.short_description = 'Duration (minutes)'