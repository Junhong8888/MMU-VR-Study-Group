import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Room, Message

class WorkspaceConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )
        await self.accept()

        # Optionally send previous messages on connect
        messages = await self.get_last_50_messages()
        for message in messages:
            await self.send(text_data=json.dumps({
                'user': message.user.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = self.scope["user"].username

        # Save message to DB
        await self.save_message(self.room_name, self.scope["user"], message)

        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'user': username,
            }
        )

    # Receive message from room group
    async def chat_message(self, event):
        message = event['message']
        user = event['user']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            'message': message,
            'user': user,
        }))

    @database_sync_to_async
    def save_message(self, room_name, user, message):
        room = Room.objects.get(roomname=room_name)
        return Message.objects.create(user=user, room=room, content=message)

    @database_sync_to_async
    def get_last_50_messages(self):
        room = Room.objects.get(roomname=self.room_name)
        return Message.objects.filter(room=room).order_by('-timestamp')[:50][::-1]
