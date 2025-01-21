from channels.db import database_sync_to_async
from channels.auth import get_user
from rest_framework.authtoken.models import Token
import urllib.parse

class TokenAuthMiddleware:
    """
    Custom middleware to handle authentication for WebSocket connections.
    """
    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        """
        This is the correct signature for middleware's __call__ method in Channels.
        The `scope` contains the connection information and should be passed to the inner application.
        """
        # Retrieve token from query params in the URL
        token_key = None
        query_string = scope.get('query_string', b'').decode()

        # Parse the query string and get the 'token' parameter
        query_params = urllib.parse.parse_qs(query_string)
        if 'token' in query_params:
            token_key = query_params['token'][0]

        if token_key:
            user = await self.authenticate_user(token_key)
            scope['user'] = user  # Add user to the scope
        else:
            scope['user'] = None  # Set user as None if no token

        # Now call the inner application with the updated scope.
        return await self.inner(scope, receive, send)

    @database_sync_to_async
    def authenticate_user(self, token_key):
        """
        Authenticate user using the provided token.
        """
        try:
            token = Token.objects.get(key=token_key)
            return token.user
        except Token.DoesNotExist:
            return None  # Return None if token is invalid
