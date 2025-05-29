import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
django.setup()

import chat.routing
import grouping.routing

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            # Removed dashboard.routing.websocket_urlpatterns
            chat.routing.websocket_urlpatterns +
            grouping.routing.websocket_urlpatterns
        )
    ),
})
