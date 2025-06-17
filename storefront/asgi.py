import os
import django
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
<<<<<<< HEAD
=======
import django

>>>>>>> deploy

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')
django.setup()

import chat.routing
import grouping.routing
<<<<<<< HEAD
=======
import workspace_chat.routing
>>>>>>> deploy

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
<<<<<<< HEAD
            # Removed dashboard.routing.websocket_urlpatterns
            chat.routing.websocket_urlpatterns +
            grouping.routing.websocket_urlpatterns
=======
            chat.routing.websocket_urlpatterns + grouping.routing.websocket_urlpatterns + workspace_chat.routing.websocket_urlpatterns
>>>>>>> deploy
        )
    ),
})
