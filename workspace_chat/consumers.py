import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from .models import ChatMessage, Workspace
from django.contrib.auth.models import AnonymousUser

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.workspace_id = self.scope['url_route']['kwargs']['workspace_id']
        self.room_group_name = f'chat_{self.workspace_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        user = self.scope["user"]

        if not isinstance(user, AnonymousUser):
            workspace = await self.get_workspace(self.workspace_id)
            await self.save_message(user, workspace, message)

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': f'{user.username}: {message}'
            }
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message']
        }))

    @database_sync_to_async
    def get_workspace(self, workspace_id):
        return Workspace.objects.get(id=workspace_id)

    @database_sync_to_async
    def save_message(self, user, workspace, message):
        ChatMessage.objects.create(user=user, workspace=workspace, content=message)


### views.py
from django.http import JsonResponse
from .models import ChatMessage

def load_messages(request, workspace_id):
    messages = ChatMessage.objects.filter(workspace_id=workspace_id).select_related('user').order_by('timestamp')
    data = [
        {'user': message.user.username, 'content': message.content, 'timestamp': message.timestamp.isoformat()}
        for message in messages
    ]
    return JsonResponse(data, safe=False)
