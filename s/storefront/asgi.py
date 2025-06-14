"""
ASGI config for storefront project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/asgi/
"""
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
import django


os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
django.setup()

import chat.routing
import grouping.routing
import workspace_chat.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns + grouping.routing.websocket_urlpatterns + workspace_chat.routing.websocket_urlpatterns
        )
    ),
})