

import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'myblog.settings')

django.setup()

from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from notification.middleware import TokenAuthMiddleware
from notification.routing import websocket_urlpatterns

application = ProtocolTypeRouter(
    {
        "http": get_asgi_application(),
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
            )
        ),
    }
)
