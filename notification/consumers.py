import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from django.core.exceptions import ObjectDoesNotExist

User = get_user_model()

class NotificationConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Get the token from the URL query parameters
        token_key = self.scope['query_string'].decode().split('=')[-1]  # Extract the token

        if not token_key:
            await self.close()  # Close connection if no token
            return

        user = await self.authenticate_user(token_key)

        if user is None:
            await self.close()  # Close connection if authentication fails
            return

        # Store the authenticated user in the consumer
        self.user = user

        # Create a unique group name for the user (using username and user ID)
        self.group_name = f"{self.user.username}-{self.user.id}"

        print(f"User: {self.user.username} connected to the WebSocket")
        print(f"Group: {self.group_name} connected to the WebSocket")

        # Join the user to the unique group
        await self.channel_layer.group_add(self.group_name, self.channel_name)

        # Accept the WebSocket connection
        await self.accept()

    async def disconnect(self, close_code):
        # Remove user from the group when disconnecting
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        notification_content = text_data_json['notification']['content']
        
        # You can process the notification or send it to the client
        await self.send(text_data=json.dumps({
            'notification': {
                'content': notification_content
            }
        }))

    async def send_notification(self, event):
        # # Handle the sending of notifications to the WebSocket
        # notification = event['notification']
        # # notification_data = event['notification']
        # await self.send(text_data=json.dumps({notification}))
        # # await self.send(text_data=json.dumps({
        # #     'notification': notification_data
        # # }))
        notification_data = event['notification']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'notification': notification_data
        }))

    @database_sync_to_async
    def authenticate_user(self, token_key):
        """
        Authenticate the user based on the provided DRF token.
        """
        try:
            # Retrieve the Token object using the provided key
            token = Token.objects.get(key=token_key)
            user = token.user  # Get the associated user
            return user
        except Token.DoesNotExist:
            return None  # Return None if the token is invalid










# import json
# from channels.generic.websocket import AsyncWebsocketConsumer

# class NotificationConsumer(AsyncWebsocketConsumer):
#     async def connect(self):
#         print("Websocket connected...")
#         self.user = self.scope['user']
#         print(f'User is: {self.user}')
#         self.group_name = f"{self.user.username}-{self.user.id}"
#         print(f'Group is: {self.group_name}')
#         # Join room group
#         await self.channel_layer.group_add(
#             self.group_name, 
#             self.channel_name
#         )
#         await self.accept()

#     async def disconnect(self, close_code):
#         print('Websocket Disconnected...')
#         await self.channel_layer.group_discard(
#             self.group_name, 
#             self.channel_name
#         )

#     async def receive(self, text_data):
#         pass

#     async def send_notification(self, event):
#         notification = event['notification']
#         await self.send(text_data=json.dumps(notification))

    