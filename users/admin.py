from django.contrib import admin
from .models import task,TaskProgressLog,ranking,video_session,note

# Register your models here.
admin.site.register(task)
admin.site.register(TaskProgressLog)
admin.site.register(ranking)
admin.site.register(video_session)
admin.site.register(note)
