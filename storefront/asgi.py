import os
import django
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
