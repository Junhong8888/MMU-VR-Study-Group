
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(default=timezone.now)
    logout_time = models.DateTimeField(null=True, blank=True)

    def duration_hours(self):
        if self.logout_time:
            delta = self.logout_time - self.login_time
            return round(delta.total_seconds() / 3600, 2)
        return 0.0

# Create your models here.
