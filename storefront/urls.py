from django.contrib import admin
from django.urls import path, include
from workspace_chat import views as chat_views
import debug_toolbar

urlpatterns = [
    path('admin/', admin.site.urls),
    path('playground/', include('playground.urls')),
    path('__debug__/', include('debug_toolbar.urls')),
    path('', include('users.urls')),
    path('users/', include('users.urls')),
    path('chat/', include('chat.urls')),
    path('grouping/', include('grouping.urls')),
    path('zfeng/', include('zfeng.urls')),
    path('dashboard/', include('dashboard.urls')),
    path('todoapp', include('todoapp.urls')),

    # These both use load_messages from workspace_chat.views
    path('load_messages/<int:workspace_id>/', chat_views.load_messages, name='load_messages'),
    path('api/chat/<int:workspace_id>/messages/', chat_views.load_messages, name='load_messages'),

    path('workspace_chat/', include('workspace_chat.urls')),
    path('users/', include('django.contrib.auth.urls')),
]
