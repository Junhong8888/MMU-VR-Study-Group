from django.db import models
from django.contrib.auth.models import User
from grouping.models import Room

# Create your models here.
class todo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='creator')
    assigned_to = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='assignee')
    todo_name = models.CharField(max_length=1000)
    due_date = models.DateField(null=True, blank=True)
    status = models.BooleanField(default=False)
    workspace = models.ForeignKey(Room,on_delete=models.CASCADE,related_name='workspace',null=True, blank=True,)

    def __str__(self):
        return self.todo_name
