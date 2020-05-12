from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter

from django.urls import path
from chat.consumers import MainConsumer

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter([
            	path("chat/<id_user>", MainConsumer),
            ]
        )
    ),
})