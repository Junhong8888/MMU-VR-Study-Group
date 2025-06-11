import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Workspace

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.workspace_id = self.scope['url_route']['kwargs']['workspace_id']
        self.room_group_name = f'chat_{self.workspace_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        user = self.scope['user']

        if user.is_anonymous:
            # Optionally reject connection or ignore anonymous messages
            return

        # Save the message to DB asynchronously
        await self.save_message(user, message, self.workspace_id)

        # Broadcast message to the room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': user.username,
            }
        )

    async def chat_message(self, event):
        # Receive message from room group
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'user': event['user'],
        }))

    @database_sync_to_async
    def save_message(self, user, message, workspace_id):
        workspace = Workspace.objects.get(id=workspace_id)
        ChatMessage.objects.create(user=user, content=message, workspace=workspace)
