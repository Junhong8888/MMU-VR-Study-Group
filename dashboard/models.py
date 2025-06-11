

from django.db import models
from django.contrib.auth.models import User ,AbstractUser
from django.utils import timezone

class UserSession(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    @property
    def duration(self):
        if self.login_time and self.logout_time:
            return (self.logout_time - self.login_time).total_seconds() / 60  # duration in minutes
        return 0
