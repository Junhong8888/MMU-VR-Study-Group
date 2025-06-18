from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'
        self.username = self.scope["user"].username  # Get the username from Django's auth system

        # Join room group
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
        data = json.loads(text_data)

        # For chat messages
        if 'message' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'username': self.username,   # Use self.username, not client-supplied
                }
            )
        elif data.get('type') == 'new-user':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'new_user',
                    'username': self.username,   # Use self.username
                }
            )
        elif data.get('type') in ['sdp', 'ice']:
            # Attach sender as the authenticated user
            data['sender'] = self.username
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': f"{data['type']}_message",
                    'data': data,
                    'sender_channel_name': self.channel_name
                }
            )
        elif data.get('type') == 'screen_share_stream':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'screen_share_stream_message',
                    'sender': self.username,
                }
            )
        elif data.get('type') == 'screen_share_stopped':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'screen_share_stopped_message',
                    'sender': self.username,
                }
            )

    async def sdp_message(self, event):
        data = event['data']
        target = data.get('target')

        if self.username == target:
            await self.send(text_data=json.dumps({
                'type': 'sdp',
                'sdp': data['sdp'],
                'sender': data['sender']
            }))

    async def ice_message(self, event):
        data = event['data']
        target = data.get('target')

        if self.username == target:
            await self.send(text_data=json.dumps({
                'type': 'ice',
                'candidate': data['candidate'],
                'sender': data['sender']
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))

    async def new_user(self, event):
        await self.send(text_data=json.dumps({
            'type': 'new-user',
            'username': event['username']
        }))

    async def screen_share_stream_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'screen_share_stream',
            'sender': event['sender'],
        }))

    async def screen_share_stopped_message(self, event):
        await self.send(text_data=json.dumps({
            'type': 'screen_share_stopped',
            'sender': event['sender'],
        }))