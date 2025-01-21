# asgi.py
import os
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from django.core.asgi import get_asgi_application
from channels.auth import AuthMiddlewareStack
from notification.routing import websocket_urlpatterns
from notification.middleware import TokenAuthMiddleware  # Import the custom middleware

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "mysite.settings")

# Initialize Django ASGI application early to ensure the AppRegistry
# is populated before importing code that may import ORM models.
django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter(
    {
        "http": django_asgi_app,
        "websocket": AllowedHostsOriginValidator(
            TokenAuthMiddleware(  # Use the custom TokenAuthMiddleware here
                AuthMiddlewareStack(URLRouter(websocket_urlpatterns))
            )
        ),
    }
)

