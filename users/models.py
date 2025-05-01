from django.db import models
from django.contrib.auth.models import User , Group

# Create your models here.
'''
    class group(models.Model):
    id = models.BigAutoField(primary_key=True)
    time = models.TimeField()
    name = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    members =  models.ManyToManyField(User,through='membership')
    
    def __str__(self):
        return f'{self.name}'
'''    
class task(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    duedate = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'

class TaskProgressLog(models.Model):
    changed_time = models.TimeField()
    status = models.CharField(max_length=100)
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    task_id = models.ForeignKey(task,on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.status}'        

class ranking(models.Model):
    time = models.TimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    status = models.CharField(max_length=100)
    duedate = models.DateField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.title}'
    
class video_session(models.Model):    
    video_url = models.CharField(max_length=100)
    start = models.TimeField()
    end = models.TimeField()
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    #group = models.ForeignKey()

    def __str__(self):
        return f'{self.id}'
    
class note(models.Model):    
    content = models.CharField(max_length=100)
    update_time = models.TimeField()
    host = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(Group,on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.id}'    

'''
class membership(models.Model):    
    id = models.IntegerField()
    joined_time = models.TimeField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    group = models.ForeignKey(group.id)

    def __str__(self):
        return f'{self.id}'
'''
