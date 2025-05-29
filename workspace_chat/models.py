from django.db import models
from django.contrib.auth.models import User

class Workspace(models.Model):
    roomname = models.CharField(max_length=100)

    def __str__(self):
        return self.roomname

class ChatMessage(models.Model):
    workspace = models.ForeignKey(Workspace, on_delete=models.CASCADE, related_name='messages')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.user.username}: {self.content[:20]}'
