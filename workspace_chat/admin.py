from django.contrib import admin
from .models import ChatMessage,Workspace


# Register your models here.
admin.site.register(ChatMessage)
admin.site.register(Workspace)