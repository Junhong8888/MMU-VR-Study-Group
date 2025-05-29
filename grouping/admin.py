from django.contrib import admin
from .models import Room,Topic

# Register your models here.
class RoomAdmin(admin.ModelAdmin):
    list_display = ('roomname', 'host', 'topic')
    filter_horizontal = ('members',)  # Allows easy member management in the admin UI




admin.site.register(Room,RoomAdmin)
admin.site.register(Topic)