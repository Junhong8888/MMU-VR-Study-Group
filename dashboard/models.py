from django.db import models
from django.contrib.auth.models import User

class UserSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    login_time = models.DateTimeField(auto_now_add=True)
    logout_time = models.DateTimeField(null=True, blank=True)

    def duration_hours(self):
        if self.logout_time:
            return round((self.logout_time - self.login_time).total_seconds() / 3600, 2)
        return 0
