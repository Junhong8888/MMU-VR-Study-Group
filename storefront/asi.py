import os
import django
from channels.routing import get_default_application
from django.core.asgi import get_asgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'storefront.settings')  # replace with your actual project name
django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import dashboard.routing  # replace 'dashboard' with your actual app name

application = ProtocolTypeRouter({
    "http": get_asgi_application(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            dashboard.routing.websocket_urlpatterns  # ensure this matches your app and routing
        )
    ),
})
