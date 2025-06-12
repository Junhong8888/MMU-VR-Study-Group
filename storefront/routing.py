from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import chat.routing
import grouping.routing
import workspace_chat.routing  # ✅ Ensure this is included

application = ProtocolTypeRouter({
    "websocket": AuthMiddlewareStack(
        URLRouter(
            chat.routing.websocket_urlpatterns +
            grouping.routing.websocket_urlpatterns +
            workspace_chat.routing.websocket_urlpatterns  # ✅ Combine all websocket routes
        )
    )
})
