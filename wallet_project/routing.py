# wallet_project/routing.py
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from channels.security.websocket import AllowedHostsOriginValidator
from django.urls import path  # Import path from django.urls
from users.consumers import NotificationConsumer

application = ProtocolTypeRouter({
    "websocket": AllowedHostsOriginValidator(
        AuthMiddlewareStack(
            URLRouter(
                [
                    path("ws/notification/", NotificationConsumer.as_asgi()),
                    # Add more paths for different consumers if needed
                ]
            )
        )
    ),
})
