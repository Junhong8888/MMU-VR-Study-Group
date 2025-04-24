from django.db import models
from django.conf import settings

# Create your models here.
class group(models.Model):
    time = models.TimeField()
    name = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.name}'
    
class task(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=100)
    description = models.CharField()
    status = models.CharField(max_length=100)
    duedate = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

class TaskProgressLog(models.Model):
    changed_time = models.TimeField()
    status = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    task_id = models.ForeignKey(task.id)
    
    def __str__(self):
        return f'{self.status}'        

class ranking(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=100)
    description = models.CharField()
    status = models.CharField(max_length=100)
    duedate = models.DateField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    group = models.ForeignKey(group.id)

    def __str__(self):
        return f'{self.title}'
    
class video_session(models.Model):    
    id = models.IntegerField()
    video_url = models.CharField(max_length=100)
    start = models.TimeField()
    end = models.TimeField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gtoup = models.ForeignKey()

    def __str__(self):
        return f'{self.id}'
    
class note(models.Model):    
    id = models.IntegerField()
    content = models.CharField(max_length=100)
    update_time = models.TimeField()
    host = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gtoup = models.ForeignKey(group.id)

    def __str__(self):
        return f'{self.id}'    

class membership(models.Model):    
    id = models.IntegerField()
    joined_time = models.TimeField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    gtoup = models.ForeignKey(group.id)

    def __str__(self):
        return f'{self.id}'
