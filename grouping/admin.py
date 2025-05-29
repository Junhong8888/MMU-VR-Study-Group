from django.contrib import admin
from .models import Room, Topic, Message

class RoomAdmin(admin.ModelAdmin):
    list_display = ('roomname', 'host', 'topic')
    filter_horizontal = ('members',)  # Manage members easily

class MessageAdmin(admin.ModelAdmin):
    list_display = ('user', 'room', 'content', 'timestamp')
    list_filter = ('room', 'user', 'timestamp')

admin.site.register(Room, RoomAdmin)
admin.site.register(Topic)
admin.site.register(Message, MessageAdmin)
