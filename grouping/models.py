from django.db import models
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string
from ckeditor.fields import RichTextField
from django.utils import timezone


# Create your models here.
class Topic(models.Model):
    name = models.CharField(max_length=200)
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name 


class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.CASCADE)
    topic = models.ForeignKey(Topic, on_delete=models.CASCADE)
    roomname = models.CharField(max_length=200)
    description = models.TextField(null=True, blank=True)
    members = models.ManyToManyField(User, related_name="members")
    date = models.DateTimeField(auto_now_add=True)
    join_code = models.CharField(max_length=6, unique=True, blank=True)

    def save(self, *args, **kwargs):
        # Generate a unique join code if it doesn't exist
        if not self.join_code:
            while True:
                code = get_random_string(length=6).upper()
                if not Room.objects.filter(join_code=code).exists():
                    self.join_code = code
                    break
        super().save(*args, **kwargs)

    def __str__(self):
        return self.roomname


class Document(models.Model):
    title = models.CharField(max_length=200)
    content = RichTextField()

    def __str__(self):
        return self.title


# New model to store chat messages in a room (workspace)
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, related_name='messages', on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} @ {self.room.roomname}: {self.content[:20]}"
