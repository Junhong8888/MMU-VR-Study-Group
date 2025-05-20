from channels.generic.websocket import AsyncWebsocketConsumer
import json

class ChatRoomConsumers(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = f'chat_{self.room_name}'

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

        if 'message' in data and 'username' in data:
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'message': data['message'],
                    'username': data['username'],
                }
            )
        elif data.get('type') == 'sdp':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'sdp_message',
                    'sdp': data['sdp'],
                    'sender_channel_name': self.channel_name
                }
            )
        elif data.get('type') == 'ice':
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'ice_message',
                    'candidate': data['candidate'],
                    'sender_channel_name': self.channel_name
                }
            )

    async def sdp_message(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'sdp',
                'sdp': event['sdp'],
            }))

    async def ice_message(self, event):
        if self.channel_name != event['sender_channel_name']:
            await self.send(text_data=json.dumps({
                'type': 'ice',
                'candidate': event['candidate'],
            }))

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({
            'message': event['message'],
            'username': event['username'],
        }))
