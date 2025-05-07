"""
ASGI config for storefront project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from django.urls import re_path
import os
from test.routing import websocket_urlpatterns as test_ws
from chat.routing import websocket_urlpatterns as chat_ws

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')

application = ProtocolTypeRouter({
    "http": get_asgi_application(),

     "websocket": AuthMiddlewareStack(
        URLRouter(
            test_ws + chat_ws   
        )
    ),
})

