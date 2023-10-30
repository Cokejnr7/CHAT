import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from asgiref.sync import sync_to_async
from .models import Message, Thread
from authentication.models import CustomUser


class ChatConsumer(AsyncWebsocketConsumer):
    # initial connection between client and server
    async def connect(self):
        me = self.scope["user"]
        other_username = self.scope["url_route"]["kwargs"]["username"]
        other_user = await sync_to_async(CustomUser.objects.get)(
            username=other_username
        )
        for key, value in self.scope.items():
            print(key, value)

        if other_user:
            self.thread = await sync_to_async(
                Thread.objects.get_or_create_personal_thread
            )(me, other_user)

            self.room_name = f"personal_thread_{self.thread.id}"

            await self.channel_layer.group_add(self.room_name, self.channel_name)
            await self.accept()

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]

        await self.store_message(message)

        await self.channel_layer.group_send(
            self.room_name, {"type": "chat_message", "message": message}
        )

    async def chat_message(self, event):
        message = event["message"]

        await self.send(text_data=json.dumps({"type": "chat", "message": message}))

    async def disconnect(self, event):
        await self.channel_layer.group_discard(self.room_name, self.channel_name)

    @database_sync_to_async
    def store_message(self, text):
        message = Message(thread=self.thread, sender=self.scope["user"], text=text)
        message.save()
